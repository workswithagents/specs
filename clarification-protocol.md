# Agent Clarification Protocol — Layer 4

**Version:** 1.0.0
**Status:** Published
**Layer:** 4 — Session (Agent OSI Model)
**License:** CC BY 4.0

## 1. Purpose

Define how an agent MUST refuse to proceed when information is ambiguous, request structured clarification, and preserve the full clarification chain for audit. No assumptions. No silent defaults.

This is the difference between "the agent guessed" and "the agent asked, was told, and acted on verifiable answers."

## 2. Design Principles

- **Refuse, don't guess.** When input is ambiguous, the agent MUST return a structured refusal, never a best-effort assumption.
- **Field-level precision.** Clarification requests reference specific fields, not generic "more detail needed."
- **Full round-trip audit.** Every ask/answer pair is timestamped, signed, and queryable.
- **Idempotent retry.** Duplicate clarifications with same session_id return the same response.
- **Framework-agnostic.** Works between Hermes, Claude Code, Codex, Copilot, and any MCP-compatible agent.

## 3. When to Refuse

An agent MUST refuse (not guess) when:

| Condition | Example | Severity |
|-----------|---------|----------|
| **Missing required field** | Component type not specified | BLOCK |
| **Ambiguous identifier** | "Use the standard one" — which standard? | BLOCK |
| **Unresolved compliance overlap** | "GDPR" selected but user hasn't confirmed it partially covers LGPD | WARN |
| **Jurisdiction mismatch** | User requesting Va.gov patterns with UK MOD compliance | BLOCK |
| **Untranslatable language** | "ar-sa" selected but no RTL layout specified | WARN |
| **Missing validation input** | Real build requested but no output directory set | BLOCK |

## 4. Clarification Schema

```json
{
  "$schema": "https://workswithagents.dev/specs/clarification-protocol.json",
  "protocol_version": "1.0.0",
  "session_id": "uuid",
  "agent_id": "wwa-scaffold-v1.0.0",
  "agent_public_key": "ed25519:abc123...",
  "timestamp": "2026-05-10T15:00:00Z",
  "status": "needs_clarification",
  "gaps": [
    {
      "id": "gap-001",
      "field": "compliance.jurisdiction",
      "severity": "BLOCK",
      "question": "JSP 440 (UK MOD) selected but deployment target is USWDS (USA). Which jurisdiction applies?",
      "context": "Compliance overlap: JSP 440 ↔ NATO STANAG. Possible UK/NATO deployment vs US system.",
      "suggestions": ["jsp-440-only", "uswds-only", "both-with-nato-stanag"],
      "blocked_operations": ["planner", "developer", "build"]
    }
  ],
  "accepted_gaps": 0,
  "blocking_gaps": 1,
  "warning_gaps": 0,
  "signature": "ed25519:signature_bytes..."
}
```

## 5. Resolution Lifecycle

```
CALLING AGENT          SCAFFOLD AGENT (MCP)
    |                        |
    |── wwa_scaffold_plan ──>|  (description, standards, languages...)
    |                        |
    |<── needs_clarification ─|  (gaps[], severity, suggestions)
    |                        |
    |── resolve_gap ────────>|  (gap_id + answer)
    |                        |
    |<── gap_resolved ───────|  (gap_id, accepted)
    |                        |
    |── resolve_gap (gap-2)─>|  ...
    |<── gap_resolved ───────|
    |                        |
    |── confirm_plan ───────>|  (all gaps resolved)
    |<── plan_accepted ──────|  (full attestation)
    |                        |
```

## 6. MCP Tools

### `wwa_clarify_check`

Validate whether a plan submission has unresolved gaps. Returns `needs_clarification` with structured gaps or `ready_to_proceed`.

```
Input:  plan_object (full plan including compliance, languages, libraries)
Output: {status, gaps[], blocking_count, warning_count}
```

### `wwa_clarify_resolve`

Submit an answer to a specific gap. Returns updated gap status.

```
Input:  session_id, gap_id, answer (string)
Output: {gap_id, status: "resolved"|"escalated", accepted_answer}
```

### `wwa_clarify_audit`

Return the full clarification chain for a session. Auditor tool.

```
Input:  session_id
Output: {clarification_chain: [{ask: {...}, answer: {...}, timestamp, signature}...]}
```

## 7. Audit Trail

Every clarification round-trip creates an immutable record:

```json
{
  "session_id": "uuid",
  "chain": [
    {
      "round": 1,
      "ask_timestamp": "2026-05-10T15:00:00Z",
      "ask_signature": "ed25519:ask_bytes...",
      "gap": {"id": "gap-001", "field": "compliance.jurisdiction", "question": "..."},
      "answer_timestamp": "2026-05-10T15:01:23Z",
      "answer": "jsp-440-only",
      "answer_signature": "ed25519:ans_bytes...",
      "resolved": true
    }
  ],
  "total_rounds": 1,
  "all_resolved": true,
  "chain_signature": "ed25519:chain_bytes..."
}
```

**An auditor can verify:**
- Agent refused to proceed when input was ambiguous
- Each gap was resolved by explicit user/agent answer
- The full chain is signed and timestamped
- No silent assumptions were made

## 8. Implementation Requirements

All WWA compliance tools MUST implement this protocol:

| Tool | Required behaviour |
|------|--------------------|
| `wwa_scaffold_plan` | Must return `needs_clarification` if gaps exist, never a partial plan |
| `wwa_scaffold_attest` | Must refuse attestation if unresolved gaps exist |
| Any generation tool | Must check clarification status before executing |

## 9. Relation to Other Protocols

| Protocol | Relationship |
|----------|-------------|
| Handoff Protocol (#8) | Handoff includes clarification chain — receiving agent sees what was asked and answered |
| Attestation Protocol (#18) | Attestation references clarification chain — "this code was generated after N clarification rounds" |
| Identity Protocol (#15) | All clarification messages signed with agent Ed25519 key |

---

## Examples

Implementation examples for this version:

| Language | File |
|----------|------|
| Python | [clarification-protocol/v1.0.0/python.md](clarification-protocol/v1.0.0/python.md) |
| TypeScript | [clarification-protocol/v1.0.0/typescript.md](clarification-protocol/v1.0.0/typescript.md) |
| cURL | [clarification-protocol/v1.0.0/curl.md](clarification-protocol/v1.0.0/curl.md) |

