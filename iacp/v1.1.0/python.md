# IACP — Python Example

Complete Python implementation of IACP — Inter-Agent Communication Protocol (v1.0.0). Stdlib only.

```python
"""
IACP v1.0.0 — Python Reference Implementation (stdlib only)

Implements the full IACP client:
  - Peer Discovery (by capability)
  - Message Sending (request/response/event/error/heartbeat)
  - Message Polling (inbox for current agent)
  - Capability Queries
  - Negotiation Workflow
"""
import json
import time
import uuid
import urllib.request
import urllib.error
from typing import Optional


class IACPClient:
    """Inter-Agent Communication Protocol client — stdlib only."""

    VALID_INTENTS = {"handoff", "query", "negotiate", "notify", "health"}
    VALID_TYPES = {"request", "response", "event", "error", "heartbeat"}

    def __init__(self, agent_id: str, api_base: str = "https://workswithagents.dev"):
        self.agent_id = agent_id
        self.api_base = api_base.rstrip("/")

    def _post(self, path: str, body: dict) -> dict:
        url = f"{self.api_base}{path}"
        data = json.dumps(body).encode()
        req = urllib.request.Request(url, data=data, method="POST",
            headers={
                "Content-Type": "application/json",
                "X-Agent-ID": self.agent_id,
            })
        try:
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            error_body = json.loads(e.read())
            raise RuntimeError(
                f"IACP error ({e.code}): {error_body.get('detail', 'unknown')}"
            )

    def _get(self, path: str) -> dict:
        url = f"{self.api_base}{path}"
        req = urllib.request.Request(url, headers={
            "X-Agent-ID": self.agent_id,
            "Accept": "application/json"
        })
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())

    # ── Peer Discovery ───────────────────────────────────

    def discover(self, capability: Optional[str] = None) -> list[dict]:
        """Discover peers by optional capability filter."""
        path = "/v1/peers"
        if capability:
            path += f"?capability={urllib.request.quote(capability)}"
        return self._get(path)

    def broadcast_presence(self, capabilities: list[str]) -> dict:
        """Announce this agent's presence and capabilities."""
        return self._post("/v1/peers/announce", {
            "agent_id": self.agent_id,
            "capabilities": capabilities,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        })

    # ── Send Message ─────────────────────────────────────

    def send(self, to_agent: str, intent: str, payload: dict,
             msg_type: str = "request", correlation_id: Optional[str] = None,
             ttl_seconds: int = 3600) -> str:
        """
        Send an IACP message. Returns message_id.

        Args:
            to_agent: Recipient agent ID
            intent: One of: handoff, query, negotiate, notify, health
            payload: Intent-specific payload dict
            msg_type: One of: request, response, event, error, heartbeat
            correlation_id: Links to a prior message in a chain
            ttl_seconds: Message time-to-live
        """
        if intent not in self.VALID_INTENTS:
            raise ValueError(f"Invalid intent '{intent}'. Use: {self.VALID_INTENTS}")
        if msg_type not in self.VALID_TYPES:
            raise ValueError(f"Invalid type '{msg_type}'. Use: {self.VALID_TYPES}")

        msg_id = str(uuid.uuid4())
        envelope = {
            "version": "1.0",
            "message_id": msg_id,
            "correlation_id": correlation_id or str(uuid.uuid4()),
            "sender": {
                "agent_id": self.agent_id,
                "identity_sig": "ed25519:placeholder-signature",
            },
            "recipient": {
                "agent_id": to_agent,
                "channel": intent,
            },
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "ttl_seconds": ttl_seconds,
            "message": {
                "type": msg_type,
                "intent": intent,
                "payload": payload,
            }
        }

        result = self._post("/v1/messages", envelope)
        return result.get("message_id", msg_id)

    # ── Poll Inbox ───────────────────────────────────────

    def poll(self, since: Optional[str] = None, limit: int = 50) -> list[dict]:
        """Poll for messages addressed to this agent."""
        path = f"/v1/messages?recipient={self.agent_id}&limit={limit}"
        if since:
            path += f"&since={since}"
        return self._get(path)

    # ── Capability Query ─────────────────────────────────

    def query_capability(self, to_agent: str,
                         capabilities: Optional[list[str]] = None,
                         max_tokens: int = 4096,
                         priority: str = "normal") -> dict:
        """Query another agent's capabilities."""
        return self._post(f"/v1/messages", {
            "version": "1.0",
            "message_id": str(uuid.uuid4()),
            "sender": {"agent_id": self.agent_id},
            "recipient": {"agent_id": to_agent},
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "message": {
                "type": "request",
                "intent": "query",
                "payload": {
                    "capabilities": capabilities or ["code_review", "testing"],
                    "max_tokens": max_tokens,
                    "priority": priority,
                }
            }
        })

    # ── Negotiation ──────────────────────────────────────

    def negotiate(self, to_agent: str, task: str, reward_credits: int,
                  deadline: str) -> dict:
        """Propose a work negotiation."""
        correlation_id = str(uuid.uuid4())
        return self._post("/v1/messages", {
            "version": "1.0",
            "message_id": str(uuid.uuid4()),
            "correlation_id": correlation_id,
            "sender": {"agent_id": self.agent_id},
            "recipient": {"agent_id": to_agent},
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "message": {
                "type": "request",
                "intent": "negotiate",
                "payload": {
                    "task": task,
                    "reward_credits": reward_credits,
                    "deadline": deadline,
                }
            }
        })

    def respond_negotiate(self, to_agent: str, correlation_id: str,
                          accept: bool, counter_offer: Optional[dict] = None) -> dict:
        """Accept or counter a negotiation proposal."""
        payload = {"accept": accept}
        if counter_offer:
            payload["counter"] = counter_offer

        return self._post("/v1/messages", {
            "version": "1.0",
            "message_id": str(uuid.uuid4()),
            "correlation_id": correlation_id,
            "sender": {"agent_id": self.agent_id},
            "recipient": {"agent_id": to_agent},
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "message": {
                "type": "response",
                "intent": "negotiate",
                "payload": payload,
            }
        })

    # ── Heartbeat ────────────────────────────────────────

    def heartbeat(self, status: str = "healthy", load: float = 0.0) -> dict:
        """Send a heartbeat to announce liveness and load."""
        return self._post("/v1/heartbeat", {
            "agent_id": self.agent_id,
            "status": status,
            "load": load,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        })


# ── Demo ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== IACP v1.0.0 Demo ===\n")

    builder = IACPClient("builder-01")
    reviewer = IACPClient("reviewer-02")

    # 1. Peer Discovery
    print("1. Discovering peers...")
    try:
        peers = builder.discover("code_review")
        print(f"   Found {len(peers)} peer(s)")
        for p in peers[:3]:
            print(f"   - {p.get('agent_id', 'unknown')}: {p.get('capabilities', [])}")
    except RuntimeError as e:
        print(f"   API call (offline): {e}")

    # 2. Broadcast Presence
    print("\n2. Broadcasting presence...")
    try:
        builder.broadcast_presence(["code_gen", "testing"])
        reviewer.broadcast_presence(["code_review", "security_audit"])
        print("   Both agents announced.")
    except RuntimeError as e:
        print(f"   API call (offline): {e}")

    # 3. Send a query message
    print("\n3. Sending capability query...")
    try:
        msg_id = builder.send(
            to_agent="reviewer-02",
            intent="query",
            payload={
                "capabilities": ["code_review", "testing"],
                "max_tokens": 4096,
                "priority": "high"
            },
            msg_type="request"
        )
        print(f"   Message sent! ID: {msg_id}")
    except RuntimeError as e:
        print(f"   API call (offline): {e}")

    # 4. Send handoff via IACP
    print("\n4. Sending handoff request via IACP envelope...")
    try:
        handoff_msg_id = builder.send(
            to_agent="reviewer-02",
            intent="handoff",
            payload={
                "task_description": "Review NHS DTAC compliance report",
                "workspace_path": "/projects/nhs-audit",
                "priority": "critical"
            }
        )
        print(f"   Handoff over IACP! ID: {handoff_msg_id}")
    except RuntimeError as e:
        print(f"   API call (offline): {e}")

    # 5. Negotiation
    print("\n5. Negotiating work...")
    try:
        builder.negotiate(
            to_agent="reviewer-02",
            task="Audit deployment config for HIPAA compliance",
            reward_credits=100,
            deadline="2026-06-21T17:00:00Z"
        )
        print("   Negotiation proposal sent.")
    except RuntimeError as e:
        print(f"   API call (offline): {e}")

    # 6. Poll inbox
    print("\n6. Polling inbox for reviewer-02...")
    try:
        inbox = reviewer.poll(limit=5)
        print(f"   Messages waiting: {len(inbox)}")
        for msg in inbox[:3]:
            sender = msg.get("sender", {}).get("agent_id", "?")
            intent = msg.get("message", {}).get("intent", "?")
            print(f"   - From: {sender} | Intent: {intent}")
    except RuntimeError as e:
        print(f"   API call (offline): {e}")

    # 7. Heartbeat
    print("\n7. Sending heartbeat...")
    try:
        builder.heartbeat(status="healthy", load=0.3)
        print("   Heartbeat sent.")
    except RuntimeError as e:
        print(f"   API call (offline): {e}")

    # 8. Error message
    print("\n8. Sending error notification...")
    try:
        builder.send(
            to_agent="reviewer-02",
            intent="notify",
            payload={
                "error_code": "CONTEXT_OVERFLOW",
                "detail": "Task context exceeds 128K token limit",
                "suggested_action": "compress_and_retry"
            },
            msg_type="error"
        )
        print("   Error notification sent.")
    except RuntimeError as e:
        print(f"   API call (offline): {e}")

    print("\n=== Demo Complete ===")
    print("All IACP message types demonstrated: query, handoff, negotiate, heartbeat, error")
```
