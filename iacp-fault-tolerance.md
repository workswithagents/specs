# IACP Fault Tolerance — Dead-Letter & Rollback Protocol

**Version:** 1.1.0  
**Status:** Draft  
**Layer:** 5 (Coordination) / 4 (Session)  
**License:** CC BY 4.0  
**Supersedes:** IACP §4.3 (failure handling)

---

## 1. Purpose

Define rigorous error handling for asymmetric inter-agent failures during IACP handoff sequences. This specification covers:

- **Timeouts**: upstream agent fails to ACK within the TTL window
- **State rejection**: downstream agent refuses the handoff state hash
- **Rollback**: clean restoration of a cached checkpoint when a handoff is abandoned mid-transit
- **Dead-letter queue**: structured error frames that preserve causal context for audit

---

## 2. Protocol Error Frames

When an IACP handoff fails, the detecting agent **MUST** emit a signed error frame to the session's dead-letter channel. All error frames conform to the IACP envelope format (§3) with `type: "error"` and a structured `error` payload.

### 2.1 ERR_HANDOFF_TIMEOUT

Emitted when the requesting agent does not receive a signed `IACP_ACK` within 5000ms of emitting `IACP_HANDOFF`.

```
{
  "type": "error",
  "protocol": "iacp-fault-tolerance/1.0",
  "session_id": "sess_a1b2c3d4",
  "from": "agent_a@workspace",
  "to": "agent_b@workspace",
  "error": {
    "code": "ERR_HANDOFF_TIMEOUT",
    "message": "Upstream agent failed to ACK within TTL window",
    "ttl_ms": 5000,
    "elapsed_ms": 5012,
    "handoff_ref": "ho_20260619T120000Z_a1b2c3",
    "last_known_state_hash": "sha256:abcd1234..."
  },
  "timestamp": "2026-06-19T12:00:05.012Z",
  "signature": "eyJhbGciOiJFZERTQSJ9..."
}
```

| Field | Type | Description |
|-------|------|-------------|
| `error.code` | string | Fixed: `ERR_HANDOFF_TIMEOUT` |
| `error.ttl_ms` | number | Configured TTL (default 5000) |
| `error.elapsed_ms` | number | Actual elapsed time before timeout |
| `error.handoff_ref` | string | Reference to the failed handoff envelope |
| `error.last_known_state_hash` | string | SHA-256 of the last confirmed state context |

### 2.2 ERR_STATE_REJECTION

Emitted when the receiving agent validates the state context hash and finds it inconsistent with its local ledger.

```
{
  "type": "error",
  "protocol": "iacp-fault-tolerance/1.0",
  "session_id": "sess_a1b2c3d4",
  "from": "agent_b@workspace",
  "to": "agent_a@workspace",
  "error": {
    "code": "ERR_STATE_REJECTION",
    "message": "State context hash mismatch — expected abc123, received def456",
    "expected_state_hash": "sha256:abc123...",
    "received_state_hash": "sha256:def456...",
    "divergence_point": 7,
    "agent_a_last_verified_step": 7,
    "agent_b_last_verified_step": 5
  },
  "timestamp": "2026-06-19T12:00:03.100Z",
  "signature": "eyJhbGciOiJFZERTQSJ9..."
}
```

| Field | Type | Description |
|-------|------|-------------|
| `error.code` | string | Fixed: `ERR_STATE_REJECTION` |
| `error.expected_state_hash` | string | Hash the receiving agent computed locally |
| `error.received_state_hash` | string | Hash the sending agent attached to the handoff |
| `error.divergence_point` | number | Step index where the two agent chains diverged |
| `error.agent_a_last_verified_step` | number | Sender's last verified chain step |
| `error.agent_b_last_verified_step` | number | Receiver's last verified chain step |

### 2.3 ERR_CHECKPOINT_UNAVAILABLE

Emitted when a rollback is requested but no cached checkpoint exists at the required step index.

```
{
  "type": "error",
  "protocol": "iacp-fault-tolerance/1.0",
  "session_id": "sess_a1b2c3d4",
  "from": "agent_a@workspace",
  "error": {
    "code": "ERR_CHECKPOINT_UNAVAILABLE",
    "message": "No checkpoint at step index 7 for rollback target",
    "requested_step": 7,
    "oldest_available_step": 3,
    "latest_available_step": 5,
    "retention_config": "checkpoint_interval=3, max_checkpoints=10"
  },
  "timestamp": "2026-06-19T12:00:06.000Z",
  "signature": "eyJhbGciOiJFZERTQSJ9..."
}
```

---

## 3. Rollback Procedure

When an agent detects an abandoned handoff (via timeout or rejection), it MUST execute the following rollback sequence:

### 3.1 Steps

1. **FREEZE** — Halt all active execution in the affected session. Do not send new messages.
2. **CHECKPOINT** — Locate the most recent cached checkpoint **before** the divergence point.
   - Checkpoints are created automatically at configurable intervals (default: every 3 steps) and on any state-mutating event.
3. **VERIFY** — Compute the SHA-256 hash of the checkpoint state. Confirm it matches the local chain's hash at that step index.
4. **RESTORE** — Load the checkpoint state into the active context. This includes:
   - Execution stack (call frames, variables)
   - Tool invocation queue (pending, in-flight, completed)
   - Session metadata (agent_id, peer_id, protocol_version)
   - Authorization tokens (if cached and still within TTL)
5. **NOTIFY** — Emit a dead-letter error frame with `ERR_HANDOFF_TIMEOUT` or `ERR_STATE_REJECTION` to the session audit log.
6. **RESUME** — Optionally re-initiate the handoff from the checkpoint step with `IACP_HANDOFF`.

→ See [implementation examples](iacp-fault-tolerance/v1.1.0/) for the complete rollback implementation and usage examples.

---

## 4. Checkpoint Retention Policy

| Parameter | Default | Description |
|-----------|---------|-------------|
| `checkpoint_interval` | 3 steps | Create a checkpoint every N steps |
| `max_checkpoints` | 10 | Maximum retained per session |
| `checkpoint_ttl` | 3600s | Auto-evict checkpoints older than this |
| `min_rollback_distance` | 1 step | Minimum rollback (cannot roll forward) |

---

## 5. Dead-Letter Queue (DLQ)

Each agent **SHOULD** maintain a local dead-letter queue of failed handoff frames. The DLQ is a bounded FIFO (default: 1,000 entries). When the DLQ overflows:

1. The oldest entry is evicted.
2. A summary frame is emitted containing the count of evicted entries.
3. The eviction is logged to the agent's audit trail.

DLQ entries are signed and timestamped. They serve as evidence for post-mortem analysis and audit.

```json
{
  "dlq": [
    {
      "code": "ERR_HANDOFF_TIMEOUT",
      "session_id": "sess_a1b2c3d4",
      "occurred_at": "2026-06-19T12:00:05.012Z",
      "handoff_ref": "ho_20260619T120000Z_a1b2c3",
      "signature": "eyJhbGciOiJFZERTQSJ9..."
    },
    {
      "code": "ERR_STATE_REJECTION",
      "session_id": "sess_e5f6g7h8",
      "occurred_at": "2026-06-19T12:01:03.100Z",
      "expected_hash": "sha256:abc123",
      "received_hash": "sha256:def456",
      "signature": "eyJhbGciOiJFZERTQSJ9..."
    }
  ],
  "overflow_count": 0,
  "max_capacity": 1000
}
```

---

## 6. Relationship to IACP

| IACP Frame | Fault-Tolerance Behavior |
|------------|-------------------------|
| `IACP_HANDOFF` | TTL clock starts. If no `IACP_ACK` in 5000ms → `ERR_HANDOFF_TIMEOUT` |
| `IACP_ACK` | Verifies state hash. Mismatch → `ERR_STATE_REJECTION` |
| `IACP_REJECT` | Normal rejection (not a failure). No error frame needed. |
| `IACP_CANCEL` | Sender-side abort. Receiver cleans up. No error frame. |

---

## 7. Rollback Diagram

```
Agent A                          Agent B
  │                                 │
  │── IACP_HANDOFF ────────────────→│
  │                                 │  (crashes here)
  │     [5000ms timeout]            │
  │                                 │
  │─→ FREEZE session                │
  │─→ FIND checkpoint (step 5)      │
  │─→ VERIFY checkpoint hash        │
  │─→ RESTORE execution stack       │
  │─→ EMIT ERR_HANDOFF_TIMEOUT      │
  │                                 │
  │    [Agent B recovers]           │
  │←──────────────── IACP_ACK       │  (late — ignored, DLQ'd)
  │                                 │
  │── IACP_HANDOFF (from step 5) ──→│
  │←──────────────── IACP_ACK       │
  │                                 │
```

---

## 8. Security Considerations

- **Replay attacks**: Every handoff carries a unique `handoff_ref` and timestamp. Late ACKs are discarded but logged to the DLQ.
- **Checkpoint integrity**: Checkpoints are SHA-256 hashed. Any tampering between creation and restore will trigger `ERR_STATE_REJECTION`.
- **Signature chain**: All error frames are Ed25519-signed. Agents must reject unsigned error frames.
- **DLQ overflow**: Eviction of old entries does not destroy signatures — the summary frame preserves the count and period.

---

*CC BY 4.0. Part of the Works With Agents protocol suite. See [IACP](/v1/specs/iacp.md) for the base handoff protocol.*

---

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.1.0 | 2026-06-20 | Moved inline implementation examples to versioned example directories. Spec definitions unchanged. |
| 1.0.0 | — | Initial specification. |

## Examples

Implementation examples for this version:

| Language | File |
|----------|------|
| Python | [iacp-fault-tolerance/v1.1.0/python.md](iacp-fault-tolerance/v1.1.0/python.md) |
| TypeScript | [iacp-fault-tolerance/v1.1.0/typescript.md](iacp-fault-tolerance/v1.1.0/typescript.md) |
| cURL | [iacp-fault-tolerance/v1.1.0/curl.md](iacp-fault-tolerance/v1.1.0/curl.md) |

