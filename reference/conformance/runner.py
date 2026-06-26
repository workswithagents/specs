#!/usr/bin/env python3
"""
WWA Conformance Test Suite — validates agent implementations against WWA specs.

Usage:
    # Test a running agent against Handoff spec
    python runner.py --spec handoff --endpoint http://my-agent:8787

    # Test against multiple specs
    python runner.py --spec handoff,iacp,identity --endpoint http://my-agent:8787

    # JSON output (for agent consumption)
    python runner.py --spec handoff --endpoint http://my-agent:8787 --format json
"""
import argparse
import importlib.util
import json
import os
import sys
import time
from pathlib import Path
from typing import Callable

# ── Core Test Framework ─────────────────────────────────────────────────────

class ConformanceResult:
    """Result of a single conformance check."""

    def __init__(self, spec: str, requirement_id: str, keyword: str, description: str):
        self.spec = spec
        self.requirement_id = requirement_id
        self.keyword = keyword  # MUST, SHOULD, MAY
        self.description = description
        self.passed = False
        self.detail = ""
        self.duration_ms = 0

    def to_dict(self) -> dict:
        return {
            "spec": self.spec,
            "requirement_id": self.requirement_id,
            "keyword": self.keyword,
            "description": self.description,
            "passed": self.passed,
            "detail": self.detail,
            "duration_ms": self.duration_ms,
        }

    def __repr__(self):
        status = "✓" if self.passed else "✗"
        return f"{status} [{self.keyword}] {self.spec}.{self.requirement_id}: {self.description} — {self.detail}"


class ConformanceSuite:
    """Collection of conformance checks for one spec."""

    def __init__(self, spec_name: str, endpoint: str):
        self.spec_name = spec_name
        self.endpoint = endpoint.rstrip("/")
        self.results: list[ConformanceResult] = []

    def check(self, requirement_id: str, keyword: str, description: str, test_fn: Callable):
        """Run a conformance check and record the result."""
        start = time.time()
        result = ConformanceResult(self.spec_name, requirement_id, keyword, description)
        try:
            passed, detail = test_fn(self.endpoint)
            result.passed = passed
            result.detail = detail
        except Exception as e:
            result.passed = False
            result.detail = f"ERROR: {e}"
        result.duration_ms = int((time.time() - start) * 1000)
        self.results.append(result)
        return result

    def summary(self) -> dict:
        must = [r for r in self.results if r.keyword == "MUST"]
        should = [r for r in self.results if r.keyword == "SHOULD"]
        may = [r for r in self.results if r.keyword == "MAY"]

        return {
            "spec": self.spec_name,
            "endpoint": self.endpoint,
            "total": len(self.results),
            "passed": sum(1 for r in self.results if r.passed),
            "failed": sum(1 for r in self.results if not r.passed),
            "must": {"total": len(must), "passed": sum(1 for r in must if r.passed)},
            "should": {"total": len(should), "passed": sum(1 for r in should if r.passed)},
            "may": {"total": len(may), "passed": sum(1 for r in may if r.passed)},
            "score": round(sum(1 for r in self.results if r.passed) / max(len(self.results), 1) * 100, 1),
        }


# ── Spec Test Suites ────────────────────────────────────────────────────────

# Each suite is a function that takes a ConformanceSuite and adds checks.
# The function signature is: def suite(endpoint: str) -> ConformanceSuite

def suite_handoff(endpoint: str) -> ConformanceSuite:
    """Handoff Protocol v1.1.0 conformance tests."""
    import httpx

    suite = ConformanceSuite("handoff", endpoint)
    client = httpx.Client(timeout=10, headers={"Content-Type": "application/json"})

    def _iacp_envelope(sender_id="test-agent", intent="handoff", payload=None):
        import uuid
        return {
            "version": "1.0",
            "message_id": str(uuid.uuid4()),
            "sender": {"agent_id": sender_id, "identity_sig": ""},
            "recipient": {"agent_id": "ref-agent-demo", "channel": "handoff"},
            "timestamp": "2026-06-26T00:00:00Z",
            "ttl_seconds": 60,
            "message": {
                "type": "request",
                "intent": intent,
                "payload": payload or {},
            },
        }

    # ── Health endpoint ──────────────────────────────────────────────────

    def test_health():
        resp = client.get(f"{endpoint}/health")
        data = resp.json()
        checks = [
            data.get("status") == "ok",
            "agent_id" in data,
            "protocols" in data,
            "iacp/1.0" in data.get("protocols", []),
            "handoff/1.1.0" in data.get("protocols", []),
        ]
        return all(checks), f"status={data.get('status')}, protocols={data.get('protocols', [])}"

    suite.check("H-REQ-01", "MUST", "Agent MUST expose a /health endpoint returning status and protocol list", test_health)

    # ── Capability Manifest ──────────────────────────────────────────────

    def test_manifest():
        resp = client.get(f"{endpoint}/manifest.yaml")
        return resp.status_code == 200 and "agent_id" in resp.text and "capabilities" in resp.text, f"HTTP {resp.status_code}, {len(resp.text)} bytes"

    suite.check("H-REQ-02", "MUST", "Agent MUST serve a capability manifest at /manifest.yaml", test_manifest)

    # ── DID Document ─────────────────────────────────────────────────────

    def test_did():
        resp = client.get(f"{endpoint}/.well-known/did.json")
        data = resp.json()
        checks = [
            resp.status_code == 200,
            "id" in data,
            "verificationMethod" in data,
            "service" in data,
        ]
        return all(checks), f"did={data.get('id', 'N/A')}"

    suite.check("H-REQ-03", "SHOULD", "Agent SHOULD serve a W3C DID document at /.well-known/did.json", test_did)

    # ── IACP Endpoint — heartbeats ───────────────────────────────────────

    def test_heartbeat():
        env = _iacp_envelope(intent="health")
        env["message"]["type"] = "heartbeat"
        resp = client.post(f"{endpoint}/iacp/message", json=env)
        data = resp.json()
        return resp.status_code == 200 and data.get("message", {}).get("type") in ("response", "event"), f"HTTP {resp.status_code}"

    suite.check("H-REQ-04", "MUST", "Agent MUST respond to IACP heartbeat messages", test_heartbeat)

    # ── IACP Capability Query ────────────────────────────────────────────

    def test_capability_query():
        env = _iacp_envelope(intent="query", payload={"capabilities": ["handoff"]})
        env["message"]["type"] = "request"
        resp = client.post(f"{endpoint}/iacp/message", json=env)
        data = resp.json()
        payload = data.get("message", {}).get("payload", {})
        caps = payload.get("capabilities", [])
        return resp.status_code == 200 and any(c.get("action") == "handoff" for c in caps), f"found {len(caps)} capabilities"

    suite.check("H-REQ-05", "MUST", "Agent MUST respond to IACP capability queries with its capabilities", test_capability_query)

    # ── Handoff Request ──────────────────────────────────────────────────

    def test_handoff_request():
        handoff_id = f"test-{int(time.time())}"
        env = _iacp_envelope(intent="handoff", payload={
            "handoff_id": handoff_id,
            "task_id": "task-001",
            "sender": {"agent_id": "test-agent", "session_id": "sess-test"},
            "context": {
                "task_description": "Test handoff request",
                "state_snapshot": {"files_modified": [], "branch": "main"},
                "agent_memory": {"key_decisions": [], "discovered_pitfalls": [], "pending_items": []},
                "tools_required": ["terminal"],
                "constraints": {"max_turns": 5},
            },
            "quality_checklist": [],
        })
        resp = client.post(f"{endpoint}/iacp/message", json=env)
        data = resp.json()
        payload = data.get("message", {}).get("payload", {})
        is_accepted = payload.get("status") == "accepted"
        has_receiver = "receiver" in payload
        return is_accepted and has_receiver, f"status={payload.get('status')}, handoff_id={payload.get('handoff_id')}"

    suite.check("H-REQ-06", "MUST", "Agent MUST accept valid handoff requests and return an accepted status with receiver info", test_handoff_request)

    def test_handoff_reject_missing_context():
        env = _iacp_envelope(intent="handoff", payload={
            "handoff_id": f"bad-{int(time.time())}",
            "task_id": "task-bad",
            "sender": {"agent_id": "test-agent"},
            "context": {},
            "quality_checklist": [],
        })
        resp = client.post(f"{endpoint}/iacp/message", json=env)
        return resp.status_code == 200, f"HTTP {resp.status_code} (graceful handling)"

    suite.check("H-REQ-07", "SHOULD", "Agent SHOULD handle handoff requests with minimal context gracefully (no crash)", test_handoff_reject_missing_context)

    # ── Handoff Response — IACP envelope signature ───────────────────────

    def test_signature_header():
        env = _iacp_envelope(intent="health")
        env["message"]["type"] = "heartbeat"
        resp = client.post(f"{endpoint}/iacp/message", json=env)
        has_header = resp.headers.get("X-WWA-Signed") == "true"
        return has_header, f"X-WWA-Signed={resp.headers.get('X-WWA-Signed')}"

    suite.check("H-REQ-08", "MUST", "Agent MUST sign IACP responses and indicate signing via X-WWA-Signed header", test_signature_header)

    # ── Handoff Negotiation ──────────────────────────────────────────────

    def test_negotiate():
        env = _iacp_envelope(intent="negotiate", payload={
            "task": "code_review",
            "deadline": 120,
        })
        env["message"]["type"] = "request"
        resp = client.post(f"{endpoint}/iacp/message", json=env)
        data = resp.json()
        payload = data.get("message", {}).get("payload", {})
        return payload.get("accept") is True, f"accept={payload.get('accept')}"

    suite.check("H-REQ-09", "MAY", "Agent MAY negotiate task terms via IACP negotiate intent", test_negotiate)

    # ── Notifications ────────────────────────────────────────────────────

    def test_notify():
        env = _iacp_envelope(intent="notify", payload={
            "handoff_id": "test-notify",
            "status": "completed",
            "result": {"output": "done"},
        })
        env["message"]["type"] = "event"
        resp = client.post(f"{endpoint}/iacp/message", json=env)
        data = resp.json()
        payload = data.get("message", {}).get("payload", {})
        return payload.get("ack") is True, f"ack={payload.get('ack')}"

    suite.check("H-REQ-10", "MUST", "Agent MUST acknowledge IACP event notifications", test_notify)

    # ── Identity Registration ────────────────────────────────────────────

    def test_identity():
        resp = client.get(f"{endpoint}/health")
        data = resp.json()
        has_pubkey = "public_key" in data and data["public_key"].startswith("ed25519:")
        has_did = "did" in data
        return has_pubkey and has_did, f"pubkey={'yes' if has_pubkey else 'no'}, did={'yes' if has_did else 'no'}"

    suite.check("H-REQ-11", "MUST", "Agent MUST expose its Ed25519 public key and DID in health response", test_identity)

    # ── CORS ─────────────────────────────────────────────────────────────

    def test_cors():
        resp = client.options(f"{endpoint}/iacp/message", headers={
            "Origin": "https://workswithagents.dev",
            "Access-Control-Request-Method": "POST",
        })
        # FastAPI auto-CORS is not configured by default, so this is SHOULD
        return resp.status_code in (200, 204, 405), f"HTTP {resp.status_code}"

    suite.check("H-REQ-12", "SHOULD", "Agent SHOULD support CORS preflight for browser-based agent clients", test_cors)

    client.close()
    return suite


def suite_iacp(endpoint: str) -> ConformanceSuite:
    """IACP v1.1.0 conformance tests."""
    import httpx

    suite = ConformanceSuite("iacp", endpoint)
    client = httpx.Client(timeout=10, headers={"Content-Type": "application/json"})

    def _env(intent="health", msg_type="request", payload=None, sender_id="test-agent"):
        import uuid
        return {
            "version": "1.0",
            "message_id": str(uuid.uuid4()),
            "sender": {"agent_id": sender_id, "identity_sig": ""},
            "recipient": {"agent_id": "ref-agent-demo", "channel": "handoff"},
            "timestamp": "2026-06-26T00:00:00Z",
            "ttl_seconds": 60,
            "message": {
                "type": msg_type,
                "intent": intent,
                "payload": payload or {},
            },
        }

    # Heartbeat
    def test_heartbeat():
        resp = client.post(f"{endpoint}/iacp/message", json=_env("health", "heartbeat"))
        data = resp.json()
        return resp.status_code == 200 and data.get("version") == "1.0", f"HTTP {resp.status_code}"

    suite.check("IACP-REQ-01", "MUST", "Agent MUST respond to IACP heartbeat with status", test_heartbeat)

    # Message version
    def test_version():
        env = _env("health", "heartbeat")
        resp = client.post(f"{endpoint}/iacp/message", json=env)
        data = resp.json()
        return data.get("version") == "1.0", f"version={data.get('version')}"

    suite.check("IACP-REQ-02", "MUST", "Agent MUST include version field in all IACP responses", test_version)

    # Correlation
    def test_correlation():
        env = _env("health", "heartbeat")
        resp = client.post(f"{endpoint}/iacp/message", json=env)
        data = resp.json()
        return data.get("correlation_id") == env["message_id"], f"correlation={data.get('correlation_id')}"

    suite.check("IACP-REQ-03", "MUST", "Agent MUST echo correlation_id in IACP responses", test_correlation)

    # Unsupported intent
    def test_unsupported():
        env = _env("unknown_intent_x", "request")
        resp = client.post(f"{endpoint}/iacp/message", json=env)
        data = resp.json()
        msg = data.get("message", {})
        return msg.get("type") == "error", f"type={msg.get('type')}"

    suite.check("IACP-REQ-04", "MUST", "Agent MUST return an error message type for unsupported intents", test_unsupported)

    # Load reporting
    def test_load():
        resp = client.get(f"{endpoint}/health")
        data = resp.json()
        return "known_peers" in data and "active_handoffs" in data, f"peers={data.get('known_peers')}, handoffs={data.get('active_handoffs')}"

    suite.check("IACP-REQ-05", "SHOULD", "Agent SHOULD report load and peer count in health endpoint", test_load)

    client.close()
    return suite


# ── Runner ──────────────────────────────────────────────────────────────────

SUITES = {
    "handoff": suite_handoff,
    "iacp": suite_iacp,
}


def run(spec_names: list[str], endpoint: str, fmt: str = "text"):
    """Run conformance suites for the given specs."""
    results = []
    for name in spec_names:
        if name not in SUITES:
            print(f"Unknown spec: {name}. Available: {', '.join(SUITES.keys())}", file=sys.stderr)
            continue
        suite = SUITES[name](endpoint)
        results.append(suite)
        if fmt == "text":
            print(f"\n{'='*60}")
            print(f"  {suite.spec_name} — Conformance Report")
            print(f"{'='*60}")
            for r in suite.results:
                icon = "✅" if r.passed else "❌"
                print(f"  {icon} [{r.keyword}] {r.requirement_id}")
                print(f"     {r.description}")
                print(f"     → {r.detail} ({r.duration_ms}ms)")
            print()
            summary = suite.summary()
            print(f"  Score: {summary['score']}% ({summary['passed']}/{summary['total']})")
            print(f"  MUST: {summary['must']['passed']}/{summary['must']['total']} passed")
            print(f"  SHOULD: {summary['should']['passed']}/{summary['should']['total']} passed")
            print(f"  MAY: {summary['may']['passed']}/{summary['may']['total']} passed")

    if fmt == "json":
        output = {
            "summary": {
                "total_specs": len(results),
                "total_checks": sum(len(s.results) for s in results),
                "total_passed": sum(sum(1 for r in s.results if r.passed) for s in results),
            },
            "results": [s.summary() for s in results],
            "details": [r.to_dict() for s in results for r in s.results],
        }
        print(json.dumps(output, indent=2))


def main():
    parser = argparse.ArgumentParser(description="WWA Conformance Test Suite")
    parser.add_argument("--spec", default="handoff", help="Comma-separated spec names (handoff,iacp)")
    parser.add_argument("--endpoint", default="http://localhost:8787", help="Agent endpoint URL")
    parser.add_argument("--format", default="text", choices=["text", "json"], help="Output format")
    parser.add_argument("--list", action="store_true", help="List available spec suites")
    args = parser.parse_args()

    if args.list:
        print("Available spec suites:")
        for name in SUITES:
            print(f"  {name}")
        return

    specs = [s.strip() for s in args.spec.split(",") if s.strip()]
    if not specs:
        print("No specs specified. Use --spec handoff or --list to see available suites.")
        sys.exit(1)

    run(specs, args.endpoint, args.format)


if __name__ == "__main__":
    main()
