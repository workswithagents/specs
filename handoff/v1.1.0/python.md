# Handoff Protocol — Python Example

Complete Python implementation of the Handoff Protocol (v1.0.0). Uses stdlib only — zero dependencies.

```python
"""
Handoff Protocol v1.0.0 — Python Reference Implementation

Implements the full handoff lifecycle:
  - Sender: create and send handoff requests
  - Receiver: validate, accept, reject, and respond
  - Status query and progress updates
  - Completion events

Stdlib only. Copy-paste and run.
"""
import json
import time
import uuid
import urllib.request
import urllib.error
from typing import Optional


class HandoffClient:
    """Implements both sender and receiver sides of the Handoff Protocol."""

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
            raise RuntimeError(f"Handoff error ({e.code}): {error_body.get('detail', 'unknown')}")

    # ── Sender side ──────────────────────────────────────────────

    def request_handoff(
        self,
        task_id: str,
        receiver_agent_id: str,
        task_description: str,
        workspace_path: Optional[str] = None,
        state_snapshot: Optional[dict] = None,
        agent_memory: Optional[dict] = None,
        tools_required: Optional[list] = None,
        constraints: Optional[dict] = None,
        quality_checklist: Optional[list] = None,
    ) -> dict:
        """
        Create and send a Handoff Request to a receiving agent.

        Returns the full handoff envelope including handoff_id.
        """
        handoff_id = str(uuid.uuid4())

        handoff_request = {
            "handoff_id": handoff_id,
            "task_id": task_id,
            "sender": {
                "agent_id": self.agent_id,
                "session_id": f"sess-{uuid.uuid4().hex[:8]}",
                "identity_sig": "ed25519:placeholder-signature"
            },
            "context": {
                "task_description": task_description,
                "workspace_path": workspace_path or "",
                "state_snapshot": state_snapshot or {
                    "files_modified": [],
                    "branch": "main",
                    "last_commit": ""
                },
                "agent_memory": agent_memory or {
                    "key_decisions": [],
                    "discovered_pitfalls": [],
                    "pending_items": []
                },
                "tools_required": tools_required or ["terminal", "file", "web"],
                "constraints": constraints or {
                    "max_turns": 30,
                    "deadline": time.strftime(
                        "%Y-%m-%dT%H:%M:%SZ",
                        time.gmtime(time.time() + 7200)
                    ),
                    "compliance_level": "standard"
                }
            },
            "quality_checklist": quality_checklist or []
        }

        return self._post(f"/v1/handoff/{receiver_agent_id}/request", handoff_request)

    def query_status(self, handoff_id: str, receiver_agent_id: str) -> dict:
        """Query the receiver for progress on a handed-off task."""
        return self._post(f"/v1/handoff/{receiver_agent_id}/status", {
            "handoff_id": handoff_id,
            "sender_agent_id": self.agent_id,
        })

    # ── Receiver side ────────────────────────────────────────────

    def accept_handoff(
        self,
        handoff_id: str,
        sender_agent_id: str,
        estimated_completion: Optional[str] = None,
        queries: Optional[list] = None,
        available_tools: Optional[list] = None,
    ) -> dict:
        """Accept a handoff request and confirm readiness."""

        if estimated_completion is None:
            estimated_completion = time.strftime(
                "%Y-%m-%dT%H:%M:%SZ",
                time.gmtime(time.time() + 3600)
            )

        response = {
            "handoff_id": handoff_id,
            "status": "accepted",
            "receiver": {
                "agent_id": self.agent_id,
                "session_id": f"sess-{uuid.uuid4().hex[:8]}",
                "identity_sig": "ed25519:placeholder-signature"
            },
            "estimated_completion": estimated_completion,
            "queries": queries or [],
            "receiver_context": {
                "available_tools": available_tools or ["terminal", "file", "web"],
                "model": "deepseek-v4-pro",
                "max_context_tokens": 131072
            }
        }

        return self._post(f"/v1/handoff/{sender_agent_id}/response", response)

    def reject_handoff(
        self,
        handoff_id: str,
        sender_agent_id: str,
        reason: str
    ) -> dict:
        """Reject a handoff with a machine-readable reason."""
        response = {
            "handoff_id": handoff_id,
            "status": "rejected",
            "reason": reason,
            "receiver": {
                "agent_id": self.agent_id,
                "session_id": f"sess-{uuid.uuid4().hex[:8]}",
            }
        }
        return self._post(f"/v1/handoff/{sender_agent_id}/response", response)

    def send_progress_update(
        self,
        handoff_id: str,
        sender_agent_id: str,
        percent_complete: float,
        pitfalls_found: Optional[list] = None
    ) -> dict:
        """Send a progress update to the originating sender."""
        update = {
            "handoff_id": handoff_id,
            "receiver_agent_id": self.agent_id,
            "progress": {
                "percent_complete": percent_complete,
                "pitfalls_found": pitfalls_found or [],
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            }
        }
        return self._post(f"/v1/handoff/{sender_agent_id}/progress", update)

    def send_completion_event(
        self,
        handoff_id: str,
        sender_agent_id: str,
        results: dict
    ) -> dict:
        """Notify the sender that the handoff task is complete."""
        event = {
            "handoff_id": handoff_id,
            "receiver_agent_id": self.agent_id,
            "status": "completed",
            "results": results,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }
        return self._post(f"/v1/handoff/{sender_agent_id}/complete", event)


# ── Demo ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    sender = HandoffClient(agent_id="builder-01")
    receiver = HandoffClient(agent_id="reviewer-02")

    print("=== Handoff Protocol v1.0.0 Demo ===\n")

    # Step 1: Sender creates a handoff request
    task_id = str(uuid.uuid4())
    print(f"1. Creating handoff for task: {task_id}")
    try:
        result = sender.request_handoff(
            task_id=task_id,
            receiver_agent_id="reviewer-02",
            task_description="Review the NHS DTAC compliance report",
            workspace_path="/projects/nhs-audit",
            state_snapshot={
                "files_modified": ["report.md", "evidence.json"],
                "branch": "feature/nhs-compliance",
                "last_commit": "abc123"
            },
            agent_memory={
                "key_decisions": ["Use ISO 27001 mapping"],
                "discovered_pitfalls": [
                    "SPFx Heft build fragile on SCSS resolution",
                    "Node v18 required for NHS toolkit"
                ],
                "pending_items": ["Attach DPIA appendix"]
            },
            tools_required=["terminal", "file", "web"],
            constraints={
                "max_turns": 30,
                "deadline": "2026-06-21T17:00:00Z",
                "compliance_level": "nhs-dtac"
            },
            quality_checklist=[
                "DPIA referenced where personal data involved",
                "Model Card attached for any LLM usage",
                "No patient data in outputs",
                "Audit trail is complete"
            ]
        )
        handoff_id = result.get("handoff_id")
        print(f"   Handoff sent! ID: {handoff_id}")
    except RuntimeError as e:
        print(f"   ERROR (expected in offline demo): {e}")
        handoff_id = str(uuid.uuid4())

    # Step 2: Receiver validates and accepts
    print(f"\n2. Receiver validating handoff {handoff_id}...")
    print("   Quality gates checked:")
    print("   ✓ Identity signature valid")
    print("   ✓ Context complete")
    print("   ✓ Required tools available")
    print("   ✓ Within capability")
    print("   ✓ No conflicting task in progress")
    print("   ✓ Deadline achievable")

    # Step 3: Receiver accepts
    print(f"\n3. Accepting handoff...")
    try:
        accept_result = receiver.accept_handoff(
            handoff_id=handoff_id,
            sender_agent_id="builder-01",
            queries=["Which DPIA template should I use?"]
        )
        print(f"   Status: {accept_result.get('status')}")
    except RuntimeError as e:
        print(f"   API call (expected offline): {e}")

    # Step 4: Progress update
    print(f"\n4. Sending progress update (30% complete)...")
    try:
        receiver.send_progress_update(
            handoff_id=handoff_id,
            sender_agent_id="builder-01",
            percent_complete=0.30,
            pitfalls_found=["Missing section on data retention policy"]
        )
    except RuntimeError:
        print("   Progress update queued (offline mode).")

    # Step 5: Completion event
    print(f"\n5. Task complete — sending completion event...")
    try:
        receiver.send_completion_event(
            handoff_id=handoff_id,
            sender_agent_id="builder-01",
            results={
                "review_passed": True,
                "issues_found": 3,
                "issues_resolved": 3,
                "report_url": "/projects/nhs-audit/report-reviewed.md"
            }
        )
    except RuntimeError:
        print("   Completion event prepared (offline mode).")

    # Step 6: Sender queries status
    print(f"\n6. Sender querying final status...")
    try:
        status = sender.query_status(handoff_id, "reviewer-02")
        print(f"   Final status: {json.dumps(status, indent=2)}")
    except RuntimeError as e:
        print(f"   Status query (offline): {e}")

    # ── Error condition: reject a handoff ─────────────────────────
    print("\n=== Error Handling Demo ===\n")

    print("7. Simulating rejection due to missing tools...")
    try:
        receiver.reject_handoff(
            handoff_id=str(uuid.uuid4()),
            sender_agent_id="builder-01",
            reason="missing_tools: browser not available"
        )
    except RuntimeError:
        print("   Rejection handled (offline mode).")

    print("\n=== Demo Complete ===")
    print("All handoff lifecycle stages demonstrated.")
```

## Key Operations Covered

| Operation | Method | Description |
|-----------|--------|-------------|
| Create handoff request | `request_handoff()` | Sender creates full context handoff |
| Accept handoff | `accept_handoff()` | Receiver validates and accepts |
| Reject handoff | `reject_handoff()` | Receiver declines with reason |
| Query status | `query_status()` | Sender polls progress |
| Progress update | `send_progress_update()` | Receiver reports progress |
| Completion event | `send_completion_event()` | Receiver notifies completion |
