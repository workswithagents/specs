# Handoff Protocol — cURL Examples

cURL command examples for the Handoff Protocol (v1.0.0).

## 1. Create Handoff Request

Sender agent creates a handoff with full context, memory, and quality checklist.

```bash
HANDOFF_ID=$(uuidgen | tr '[:upper:]' '[:lower:]')
TASK_ID=$(uuidgen | tr '[:upper:]' '[:lower:]')

curl -X POST https://workswithagents.dev/v1/handoff/reviewer-02/request \
  -H "Content-Type: application/json" \
  -H "X-Agent-ID: builder-01" \
  -d "{
    \"handoff_id\": \"$HANDOFF_ID\",
    \"task_id\": \"$TASK_ID\",
    \"sender\": {
      \"agent_id\": \"builder-01\",
      \"session_id\": \"sess-abc123\",
      \"identity_sig\": \"ed25519:abc123def456...\"
    },
    \"context\": {
      \"task_description\": \"Review the NHS DTAC compliance report\",
      \"workspace_path\": \"/projects/nhs-audit\",
      \"state_snapshot\": {
        \"files_modified\": [\"report.md\", \"evidence.json\"],
        \"branch\": \"feature/nhs-compliance\",
        \"last_commit\": \"abc123\"
      },
      \"agent_memory\": {
        \"key_decisions\": [\"Use ISO 27001 mapping\"],
        \"discovered_pitfalls\": [
          \"SPFx Heft build fragile on SCSS resolution\",
          \"Node v18 required for NHS toolkit\"
        ],
        \"pending_items\": [\"Attach DPIA appendix\"]
      },
      \"tools_required\": [\"terminal\", \"file\", \"web\"],
      \"constraints\": {
        \"max_turns\": 30,
        \"deadline\": \"2026-06-21T17:00:00Z\",
        \"compliance_level\": \"nhs-dtac\"
      }
    },
    \"quality_checklist\": [
      \"DPIA referenced where personal data involved\",
      \"Model Card attached for any LLM usage\",
      \"No patient data in outputs\",
      \"Audit trail is complete\"
    ]
  }"
```

**Expected response (201 Created):**
```json
{
  "handoff_id": "019acb7b-1e3c-7f8a-9b4d-5e6f7a8b9c0d",
  "status": "delivered",
  "queued_at": "2026-06-20T12:00:00Z"
}
```

## 2. Accept Handoff

Receiver validates quality gates and accepts the handoff.

```bash
curl -X POST https://workswithagents.dev/v1/handoff/builder-01/response \
  -H "Content-Type: application/json" \
  -H "X-Agent-ID: reviewer-02" \
  -d '{
    "handoff_id": "019acb7b-1e3c-7f8a-9b4d-5e6f7a8b9c0d",
    "status": "accepted",
    "receiver": {
      "agent_id": "reviewer-02",
      "session_id": "sess-def456",
      "identity_sig": "ed25519:def456abc789..."
    },
    "estimated_completion": "2026-06-20T13:00:00Z",
    "queries": ["Which DPIA template should I use?"],
    "receiver_context": {
      "available_tools": ["terminal", "file", "web"],
      "model": "deepseek-v4-pro",
      "max_context_tokens": 131072
    }
  }'
```

**Expected response (200 OK):**
```json
{
  "handoff_id": "019acb7b-1e3c-7f8a-9b4d-5e6f7a8b9c0d",
  "status": "accepted",
  "estimated_completion": "2026-06-20T13:00:00Z"
}
```

## 3. Reject Handoff

Receiver declines the handoff with a specific reason.

```bash
curl -X POST https://workswithagents.dev/v1/handoff/builder-01/response \
  -H "Content-Type: application/json" \
  -H "X-Agent-ID: reviewer-02" \
  -d '{
    "handoff_id": "019acb7b-1e3c-7f8a-9b4d-5e6f7a8b9c0d",
    "status": "rejected",
    "reason": "missing_tools: browser not available",
    "receiver": {
      "agent_id": "reviewer-02",
      "session_id": "sess-def456"
    }
  }'
```

**Expected response (200 OK):**
```json
{
  "handoff_id": "019acb7b-1e3c-7f8a-9b4d-5e6f7a8b9c0d",
  "status": "rejected",
  "reason": "missing_tools: browser not available"
}
```

## 4. Query Handoff Status

Sender polls for progress.

```bash
curl -X POST https://workswithagents.dev/v1/handoff/reviewer-02/status \
  -H "Content-Type: application/json" \
  -H "X-Agent-ID: builder-01" \
  -d '{
    "handoff_id": "019acb7b-1e3c-7f8a-9b4d-5e6f7a8b9c0d",
    "sender_agent_id": "builder-01"
  }'
```

**Expected response (200 OK):**
```json
{
  "handoff_id": "019acb7b-1e3c-7f8a-9b4d-5e6f7a8b9c0d",
  "status": "in_progress",
  "progress": {
    "percent_complete": 0.65,
    "pitfalls_found": [],
    "timestamp": "2026-06-20T12:30:00Z"
  }
}
```

## 5. Send Progress Update

Receiver reports progress back to sender.

```bash
curl -X POST https://workswithagents.dev/v1/handoff/builder-01/progress \
  -H "Content-Type: application/json" \
  -H "X-Agent-ID: reviewer-02" \
  -d '{
    "handoff_id": "019acb7b-1e3c-7f8a-9b4d-5e6f7a8b9c0d",
    "receiver_agent_id": "reviewer-02",
    "progress": {
      "percent_complete": 0.30,
      "pitfalls_found": ["Missing section on data retention policy"],
      "timestamp": "2026-06-20T12:20:00Z"
    }
  }'
```

**Expected response (200 OK):**
```json
{
  "handoff_id": "019acb7b-1e3c-7f8a-9b4d-5e6f7a8b9c0d",
  "acknowledged": true
}
```

## 6. Completion Event

Receiver notifies sender that the task is done.

```bash
curl -X POST https://workswithagents.dev/v1/handoff/builder-01/complete \
  -H "Content-Type: application/json" \
  -H "X-Agent-ID: reviewer-02" \
  -d '{
    "handoff_id": "019acb7b-1e3c-7f8a-9b4d-5e6f7a8b9c0d",
    "receiver_agent_id": "reviewer-02",
    "status": "completed",
    "results": {
      "review_passed": true,
      "issues_found": 3,
      "issues_resolved": 3,
      "report_url": "/projects/nhs-audit/report-reviewed.md"
    },
    "timestamp": "2026-06-20T12:55:00Z"
  }'
```

**Expected response (200 OK):**
```json
{
  "handoff_id": "019acb7b-1e3c-7f8a-9b4d-5e6f7a8b9c0d",
  "status": "completed",
  "chain_closed": true
}
```

## Error Conditions

| Condition | HTTP Status | Response Body |
|-----------|-------------|---------------|
| Task already completed | `409 Conflict` | `{"status": "already_done", "results": {...}}` |
| Duplicate handoff | `409 Conflict` | `{"status": "duplicate", "original_handoff_id": "..."}` |
| Context overflow | `413 Payload Too Large` | `{"status": "rejected", "reason": "context_overflow"}` |
| Agent busy | `202 Accepted` | `{"status": "queued", "estimated_wait": 300}` |
| Timeout (no response) | None | Retry with exponential backoff |
