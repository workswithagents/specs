"""
WWA Reference Agent — reference implementation of the WWA protocol stack.

Implements:
- IACP (Inter-Agent Communication Protocol) v1.1.0
- Handoff Protocol v1.1.0
- Identity Protocol v1.1.0 (Ed25519)
- Capability Manifest v1.1.0
- Registry auto-registration

Usage:
    docker compose up
    # or standalone:
    pip install fastapi uvicorn pydantic cryptography httpx
    python main.py
"""
import json
import logging
import os
import secrets
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

import httpx
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, PlainTextResponse, Response
from pydantic import BaseModel, Field

# ── Config ──────────────────────────────────────────────────────────────────

AGENT_ID = os.getenv("WWA_AGENT_ID", f"ref-agent-{secrets.token_hex(4)}")
HOST = os.getenv("WWA_HOST", "0.0.0.0")
PORT = int(os.getenv("WWA_PORT", "8787"))
REGISTRY_URL = os.getenv("WWA_REGISTRY_URL", "https://registry.workswithagents.dev")
ENDPOINT = os.getenv("WWA_ENDPOINT", f"http://{HOST}:{PORT}")
DATA_DIR = Path(os.getenv("WWA_DATA_DIR", "/data"))
DATA_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(levelname)s %(message)s")
log = logging.getLogger("wwa-ref-agent")

# ── Identity (Ed25519) ──────────────────────────────────────────────────────

class AgentIdentity:
    """Ed25519 keypair + DID for this agent (Identity Protocol v1.1.0)."""

    def __init__(self):
        key_path = DATA_DIR / "identity.key"
        if key_path.exists():
            with open(key_path, "rb") as f:
                self._private = serialization.load_ssh_private_key(f.read(), password=None)
        else:
            self._private = ed25519.Ed25519PrivateKey.generate()
            with open(key_path, "wb") as f:
                f.write(self._private.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.OpenSSH,
                    encryption_algorithm=serialization.NoEncryption(),
                ))
        self._public = self._private.public_key()
        self.agent_id = AGENT_ID
        self.did = f"did:wwa:{AGENT_ID}"
        self.public_key_hex = self._public.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw,
        ).hex()

    def sign(self, payload: dict) -> str:
        """Sign a payload dict with Ed25519. Returns hex-encoded signature."""
        msg = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
        return self._private.sign(msg).hex()

    def verify(self, payload: dict, signature_hex: str, public_key_hex: str) -> bool:
        """Verify a payload signature. Returns True if valid."""
        try:
            pub_bytes = bytes.fromhex(public_key_hex)
            pub = ed25519.Ed25519PublicKey.from_public_bytes(pub_bytes)
            msg = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
            pub.verify(bytes.fromhex(signature_hex), msg)
            return True
        except Exception:
            return False

    def to_registration(self) -> dict:
        return {
            "identity_version": "1.1.0",
            "agent_id": self.agent_id,
            "public_key": f"ed25519:{self.public_key_hex}",
            "did": self.did,
            "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "owner": {"name": "WWA Reference Agent", "contact": "https://github.com/workswithagents/specs"},
        }


identity = AgentIdentity()

# ── State ───────────────────────────────────────────────────────────────────

handoff_store: dict[str, dict] = {}  # handoff_id → state
peer_store: dict[str, dict] = {}     # agent_id → {capabilities, endpoint, last_seen}
start_time = time.time()

# ── Pydantic Models ─────────────────────────────────────────────────────────

class IACPEnvelope(BaseModel):
    version: str = "1.0"
    message_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    correlation_id: str | None = None
    sender: dict
    recipient: dict
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    ttl_seconds: int = 3600
    message: dict


class HandoffRequest(BaseModel):
    handoff_id: str
    task_id: str
    sender: dict
    context: dict
    quality_checklist: list[str] = []


class HandoffResponse(BaseModel):
    handoff_id: str
    status: str  # accepted | rejected | completed | failed
    receiver: dict = {}
    estimated_completion: str | None = None
    queries: list[str] = []
    result: dict = {}
    error: str | None = None

# ── App ─────────────────────────────────────────────────────────────────────

app = FastAPI(
    title=f"WWA Reference Agent — {AGENT_ID}",
    version="1.0.0",
    docs_url=None,
    redoc_url=None,
)

# ── Middleware ───────────────────────────────────────────────────────────────

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    elapsed = int((time.time() - start) * 1000)
    log.info("%s %s → %s (%dms)", request.method, request.url.path, response.status_code, elapsed)
    response.headers["X-WWA-Agent-Id"] = AGENT_ID
    response.headers["X-WWA-Protocol"] = "iacp-1.0"
    return response

# ── Endpoints ───────────────────────────────────────────────────────────────

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "agent_id": AGENT_ID,
        "did": identity.did,
        "public_key": f"ed25519:{identity.public_key_hex}",
        "uptime_seconds": int(time.time() - start_time),
        "active_handoffs": len([h for h in handoff_store.values() if h.get("status") in ("accepted", "in_progress")]),
        "known_peers": len(peer_store),
        "registered": registered,
        "protocols": ["iacp/1.0", "handoff/1.1.0", "identity/1.1.0", "capability-manifest/1.1.0"],
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }


@app.get("/manifest.yaml", response_class=PlainTextResponse)
async def manifest():
    """Serve capability manifest (YAML format)."""
    return MANIFEST_YAML


@app.get("/.well-known/did.json")
async def did_document():
    """W3C DID Document (.well-known/did.json)."""
    return {
        "@context": ["https://www.w3.org/ns/did/v1"],
        "id": identity.did,
        "verificationMethod": [{
            "id": f"{identity.did}#keys-1",
            "type": "Ed25519VerificationKey2020",
            "controller": identity.did,
            "publicKeyMultibase": f"z{identity.public_key_hex}",
        }],
        "authentication": [f"{identity.did}#keys-1"],
        "assertionMethod": [f"{identity.did}#keys-1"],
        "service": [{
            "id": f"{identity.did}#iacp",
            "type": "IACPEndpoint",
            "serviceEndpoint": f"http://{HOST}:{PORT}/iacp/message",
        }],
    }


@app.post("/iacp/message")
async def iacp_message(envelope: IACPEnvelope) -> JSONResponse:
    """
    IACP message handler (IACP v1.1.0).
    Receives and processes IACP envelopes, routes to the right handler.
    """
    msg_type = envelope.message.get("type", "")
    intent = envelope.message.get("intent", "")

    log.info("IACP %s/%s from %s", msg_type, intent, envelope.sender.get("agent_id", "?"))

    # Track peer
    peer_store[envelope.sender.get("agent_id", "?")] = {
        "capabilities": envelope.sender.get("capabilities", []),
        "last_seen": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    # Route
    if msg_type == "heartbeat" and intent == "health":
        return _handle_heartbeat(envelope)
    elif msg_type == "request" and intent == "query":
        return _handle_query(envelope)
    elif msg_type == "request" and intent == "handoff":
        return _handle_handoff_request(envelope)
    elif msg_type == "request" and intent == "negotiate":
        return _handle_negotiate(envelope)
    elif msg_type == "event" and intent == "notify":
        return _handle_notify(envelope)
    else:
        return _iacp_response(envelope, "error", {
            "code": "UNSUPPORTED",
            "message": f"Unsupported message type/intent: {msg_type}/{intent}",
        })

# ── Handlers ────────────────────────────────────────────────────────────────

def _handle_heartbeat(envelope: IACPEnvelope) -> JSONResponse:
    return _iacp_response(envelope, "response", {
        "capabilities": [c["action"] for c in CAPABILITIES],
        "load": min(1.0, len(handoff_store) / 10),
        "eta_seconds": 30,
        "status": "healthy",
    })


def _handle_query(envelope: IACPEnvelope) -> JSONResponse:
    requested = envelope.message.get("payload", {}).get("capabilities", [])
    matched = [c for c in CAPABILITIES if not requested or c["action"] in requested]
    return _iacp_response(envelope, "response", {
        "capabilities": matched,
        "load": min(1.0, len(handoff_store) / 10),
        "eta_seconds": 30,
    })


def _handle_handoff_request(envelope: IACPEnvelope) -> JSONResponse:
    payload = envelope.message.get("payload", {})
    handoff = HandoffRequest(**payload)

    # Verify sender identity signature
    sender_sig = envelope.sender.get("identity_sig", "")
    if sender_sig:
        # In production, fetch public key from registry. For reference, we trust.
        log.info("Handoff from %s with signature: %s…", handoff.sender.get("agent_id", "?"), sender_sig[:16])

    # Store handoff
    context = payload.get("context", {})
    handoff_store[handoff.handoff_id] = {
        "handoff_id": handoff.handoff_id,
        "task_id": handoff.task_id,
        "sender": handoff.sender,
        "context": context,
        "quality_checklist": handoff.quality_checklist,
        "status": "accepted",
        "accepted_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    log.info("Handoff accepted: %s (task: %s)", handoff.handoff_id, handoff.task_id)

    return _iacp_response(envelope, "response", {
        "handoff_id": handoff.handoff_id,
        "status": "accepted",
        "receiver": {
            "agent_id": identity.agent_id,
            "session_id": f"sess-{secrets.token_hex(8)}",
            "identity_sig": identity.sign({"handoff_id": handoff.handoff_id, "status": "accepted"}),
        },
        "estimated_completion": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "queries": [],
    })


def _handle_negotiate(envelope: IACPEnvelope) -> JSONResponse:
    payload = envelope.message.get("payload", {})
    log.info("Negotiation from %s: %s", envelope.sender.get("agent_id", "?"), json.dumps(payload, indent=2)[:200])
    return _iacp_response(envelope, "response", {
        "accept": True,
        "counter": None,
        "eta_seconds": payload.get("deadline", 60),
    })


def _handle_notify(envelope: IACPEnvelope) -> JSONResponse:
    payload = envelope.message.get("payload", {})
    handoff_id = payload.get("handoff_id", "")
    status = payload.get("status", "")

    if handoff_id and handoff_id in handoff_store:
        handoff_store[handoff_id]["status"] = status
        log.info("Handoff %s updated to %s", handoff_id, status)

    return _iacp_response(envelope, "event", {"ack": True, "status": "received"})


def _iacp_response(envelope: IACPEnvelope, msg_type: str, payload: dict) -> JSONResponse:
    """Build a response IACP envelope."""
    resp = {
        "version": "1.0",
        "message_id": str(uuid.uuid4()),
        "correlation_id": envelope.message_id,
        "sender": {
            "agent_id": identity.agent_id,
            "identity_sig": identity.sign({
                "correlation_id": envelope.message_id,
                "type": msg_type,
                "payload": payload,
            }),
        },
        "recipient": {"agent_id": envelope.sender.get("agent_id", "unknown")},
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "ttl_seconds": 60,
        "message": {
            "type": msg_type,
            "intent": envelope.message.get("intent", "query"),
            "payload": payload,
        },
    }
    return JSONResponse(content=resp, headers={"X-WWA-Signed": "true"})

# ── Registry Registration ───────────────────────────────────────────────────

registered = False

async def register():
    """Register this agent with the WWA registry on startup."""
    global registered
    reg_data = identity.to_registration()
    reg_data["endpoint"] = ENDPOINT
    reg_data["capabilities"] = [c["action"] for c in CAPABILITIES]
    reg_data["manifest_url"] = f"{ENDPOINT}/manifest.yaml"

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(f"{REGISTRY_URL}/v1/identity", json=reg_data)
            if resp.status_code in (200, 201):
                registered = True
                log.info("Registered with registry at %s as %s", REGISTRY_URL, AGENT_ID)
            else:
                log.warning("Registry registration returned %s: %s", resp.status_code, resp.text[:200])
    except Exception as e:
        log.warning("Registry registration failed (non-fatal): %s", e)


async def deregister():
    """Deregister from the WWA registry on shutdown."""
    if registered:
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                await client.delete(f"{REGISTRY_URL}/v1/identity/{AGENT_ID}")
                log.info("Deregistered from registry")
        except Exception:
            pass


@app.on_event("startup")
async def startup():
    await register()


@app.on_event("shutdown")
async def shutdown():
    await deregister()

# ── Capabilities ────────────────────────────────────────────────────────────

CAPABILITIES = [
    {"action": "handoff", "target": "any", "description": "Receive and process task handoffs", "max_concurrent": 5},
    {"action": "query", "target": "capabilities", "description": "Respond to capability queries", "max_concurrent": 20},
    {"action": "negotiate", "target": "work", "description": "Negotiate task acceptance", "max_concurrent": 5},
    {"action": "heartbeat", "target": "health", "description": "Report health and load", "max_concurrent": 50},
]

MANIFEST_YAML = f"""# WWA Capability Manifest v1.1.0
# Generated by WWA Reference Agent

manifest_version: "1.1.0"
agent_id: "{AGENT_ID}"
agent_type: "wwa-reference"
did: "{identity.did}"

capabilities:
"""

for c in CAPABILITIES:
    MANIFEST_YAML += f"""  - action: "{c['action']}"
    target: "{c['target']}"
    description: "{c['description']}"
    max_concurrent: {c['max_concurrent']}
"""

MANIFEST_YAML += f"""
resources:
  min_tokens_per_task: 1000
  max_tokens_per_task: 50000
  preferred_model: "any"
  required_tools: ["iacp", "handoff"]

endpoint: "{ENDPOINT}"
public_key: "ed25519:{identity.public_key_hex}"
registered: $REGISTERED

identity:
  did: "{identity.did}"
  verification_method: "Ed25519VerificationKey2020"
  service_endpoint: "{ENDPOINT}/iacp/message"
"""

# ── Main ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT, log_level="info")
