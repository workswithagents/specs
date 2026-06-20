# Agent Registry — L3 Discovery / L7 Governance

**Version:** 1.0.0
**Status:** Published
**Layer:** 3 (Discovery) / 7 (Governance) — Agent OSI Model
**License:** CC BY 4.0

---

## 1. Purpose

A central registry of every AI agent operating in an environment. The registry answers:

- Who is allowed to act?
- What capabilities do they have?
- What is their current status?
- What have they done?

The Agent Registry is the **identity layer's runtime counterpart**. The [Identity Protocol](identity.md) handles cryptographic key binding and message signing. The Registry adds: lifecycle management, discovery, capability declaration, status transitions, and audit history.

Without a registry, you have anonymous agents making unverifiable claims about who they are. With a registry, every agent has a verifiable record.

---

## 2. Design Principles

- **Registry as source of truth.** Every agent registers before acting. No deviation. The registry is the authoritative record of allowed agents.
- **Identity-backed.** Registry entries are linked to Ed25519 keypairs via the Identity Protocol. No key, no entry.
- **Status-driven lifecycle.** Agents transition through explicit states: active → rotating → suspended → revoked. Each transition is logged.
- **Discovery-enabled.** The registry exposes a query interface so other agents can discover capabilities and verify identities before delegating.
- **Framework-agnostic.** Any agent framework can register. The schema is simple, the API is REST + signed messages.

---

## 3. Registry Schema

```yaml
# Agent Registry Entry
agent_id: "deploy-bot-v2"               # unique, human-readable
identity_ref:                            # link to Identity Protocol
  public_key: "ed25519:abc123def456..."
  key_fingerprint: "sha256:f1d2..."       # for quick verification
  identity_version: "1.0.0"
created_at: "2026-05-26T12:00:00Z"
updated_at: "2026-05-26T14:30:00Z"

status:
  current: "active"                      # active | rotating | suspended | revoked
  previous: "active"                     # for change tracking
  changed_at: "2026-05-26T14:30:00Z"
  changed_by: "admin@workswithagents.dev"

owner:                                    # responsible human or team
  type: "user"                            # user | team | service
  id: "agent@example.com"
  proof: "signed-challenge-response..."   # optional: cryptographic proof of ownership

capabilities:                             # what this agent can do
  - "deploy:staging"
  - "deploy:production"                   # explicit scope
  - "api:model-inference"
  tools:
    - "terminal"
    - "patch"
    - "delegate_task"
  models:
    - "claude-sonnet-4"
    - "gpt-4o"

metadata:
  version: "2.1.0"
  framework: "Hermes Agent"
  host: "build-server-01.internal"
  environment: "production"
  tags:
    - "deployment"
    - "ci-cd"
```

---

## 4. Status Model

```
                 ┌──────────┐
                 │ CREATED  │  (not yet registered)
                 └────┬─────┘
                      │ register()
                      ▼
              ┌───────────────┐
         ┌─── │    ACTIVE     │ ◄──────────────┐
         │    └───────┬───────┘                │
         │            │                        │
         │      rotate()                 unsuspend()
         │            │                        │
         │            ▼                        │
         │    ┌───────────────┐         ┌──────┴───────┐
         └─── │   ROTATING    │         │  SUSPENDED   │
              └───────┬───────┘         └──────┬───────┘
                      │                        │
                 24h expiry               escalate()
                      │                        │
                      ▼                        ▼
              ┌──────────────────────────────────────┐
              │              REVOKED                  │
              └──────────────────────────────────────┘
```

| Status | Meaning | Transitions | Duration |
|--------|---------|-------------|----------|
| **Created** | Keypair exists but not registered | → Active (on register) | Instant |
| **Active** | Agent can act, accept delegations, and be discovered | → Rotating, Suspended, Revoked | Indefinite |
| **Rotating** | Key rotation in progress. Old key accepted for 24h, new key active. | → Active (rotation complete), → Revoked (if old key compromised) | Max 24h |
| **Suspended** | Temporary pause. Agent cannot act but record persists. | → Active (unsuspended) | Configurable |
| **Revoked** | Permanent invalidation. Agent cannot act, all pending tasks reassigned. | Terminal | Permanent |

---

## 5. API

### Register

```http
POST /v1/registry/register
Content-Type: application/json

{
  "agent_id": "deploy-bot-v2",
  "public_key": "ed25519:abc123def456...",
  "capabilities": ["deploy:staging", "deploy:production"],
  "owner": "agent@example.com",
  "signature": "ed25519:base64signed..."  // signed by agent's private key
}

→ 201 Created
{
  "agent_id": "deploy-bot-v2",
  "status": "active",
  "registered_at": "2026-05-26T12:00:00Z"
}
```

### Get (Discovery)

```http
GET /v1/registry/{agent_id}

→ 200 OK
{
  "agent_id": "deploy-bot-v2",
  "public_key": "ed25519:abc123def456...",
  "capabilities": ["deploy:staging", "deploy:production"],
  "status": "active",
  "owner": "agent@example.com",
  "registered_at": "2026-05-26T12:00:00Z"
}
```

### Query (Discovery)

```http
GET /v1/registry?capability=deploy:staging&status=active

→ 200 OK
{
  "agents": [
    {
      "agent_id": "deploy-bot-v2",
      "capabilities": ["deploy:staging", "deploy:production"],
      "status": "active"
    },
    {
      "agent_id": "deploy-bot-legacy",
      "capabilities": ["deploy:staging"],
      "status": "active"
    }
  ]
}
```

### Update Capabilities

```http
PATCH /v1/registry/{agent_id}/capabilities
Content-Type: application/json

{
  "capabilities": ["deploy:staging", "deploy:production", "monitor:health"],
  "signature": "ed25519:base64signed..."
}

→ 200 OK
{
  "agent_id": "deploy-bot-v2",
  "capabilities": ["deploy:staging", "deploy:production", "monitor:health"],
  "updated_at": "2026-05-26T14:30:00Z"
}
```

### Rotate

```http
POST /v1/registry/{agent_id}/rotate
Content-Type: application/json

{
  "new_public_key": "ed25519:newkey456...",
  "signed_by_old_key": "ed25519:base64signed...",
  "reason": "scheduled rotation"
}

→ 200 OK
{
  "agent_id": "deploy-bot-v2",
  "status": "rotating",
  "old_key_expires": "2026-05-27T14:30:00Z"
}
```

### Suspend / Unsuspend

```http
POST /v1/registry/{agent_id}/suspend
Content-Type: application/json

{
  "reason": "security review — credential proxy audit",
  "initiated_by": "admin@workswithagents.dev"
}

→ 200 OK
{
  "agent_id": "deploy-bot-v2",
  "status": "suspended",
  "suspended_at": "2026-05-26T15:00:00Z"
}
```

### Revoke

```http
POST /v1/registry/{agent_id}/revoke
Content-Type: application/json

{
  "reason": "agent compromised — unexpected EC2 instance creation",
  "initiated_by": "admin@workswithagents.dev",
  "reassign_pending": true
}

→ 200 OK
{
  "agent_id": "deploy-bot-v2",
  "status": "revoked",
  "revoked_at": "2026-05-26T15:30:00Z",
  "pending_tasks_reassigned": 3
}
```

### Audit Log

Every registry operation produces an immutable audit entry:

```yaml
audit_entry:
  registry_action: "revoke"
  agent_id: "deploy-bot-v2"
  timestamp: "2026-05-26T15:30:00Z"
  initiated_by: "admin@workswithagents.dev"
  reason: "agent compromised — unexpected EC2 instance creation"
  previous_status: "active"
  new_status: "revoked"
  signature: "ed25519:base64auditsignature..."
```

The audit log is append-only, signed, and linked to the previous entry (hash chain). This makes it tamper-evident — any deletion or modification breaks the chain.

---

## 6. Threat Model

| Threat | Protection |
|--------|-----------|
| **Impersonation** (agent claims a false identity) | Registration requires signature verification against public key. Registry checks every request against the registered key. |
| **Unauthorised registration** (bad actor registers a fake agent) | Registration requires owner proof (signed challenge-response, or admin token). Unknown signers are rejected. |
| **Stale agents** (revoked agent continues operating) | Gateway checks registry status before every action. Revoked → request rejected. Heartbeat monitoring alerts on stale agents. |
| **Registry compromise** | Registry only stores public keys and metadata — no secrets. Audit log provides tamper-evident reconstruction. |
| **Capability creep** (agent claims capabilities it shouldn't have) | Capability changes require admin approval or a signed delegation from the owner. Registry doesn't trust self-reported expansions. |
| **Key theft with rotation** (attacker steals key, rotates it, keeps access) | Old-key-signed rotation prevents unauthorised rotation. Hardware binding (TPM) for enterprise. |

---

## 7. Relationship to Identity Protocol

The Agent Registry extends the Identity Protocol. Identity gives you cryptography. The Registry gives you lifecycle.

| Aspect | Identity Protocol | Agent Registry |
|--------|------------------|----------------|
| **What** | Ed25519 key binding, signature verification | Agent lifecycle, status, capabilities, discovery |
| **When** | Session creation, message signing | Before action, during delegation, after incidents |
| **Where** | In the message | In a central store |
| **Status** | Key is valid or not | Agent is active/rotating/suspended/revoked |
| **Audit** | Per-message signatures | Per-lifecycle-event entries |

**Combined flow:**
1. Agent generates Ed25519 keypair (Identity Protocol)
2. Agent registers public key + capabilities in Registry (Agent Registry)
3. Agent signs messages with private key (Identity Protocol)
4. Recipient checks registry for status (Agent Registry)
5. Recipient verifies signature against registered public key (Identity Protocol)

---

## 8. Registry Deployment Patterns

### Embedded (Single Process)
For a single-agent system on one machine. The registry is a local file or SQLite database. Simple, no network dependency.

### Centralised (Team / Organisation)
A REST API + database shared across a team's agents. Agents register once, discover each other, and the team has a single source of truth for who's operating.

### Federated (Multi-Organisation)
Multiple registries that trust each other's signatures. Agent A in Org 1 delegates to Agent B in Org 2 — Org 1's registry queries Org 2's registry to verify Agent B's identity and status. Cross-signing establishes trust between registries.

---

## 9. Agent Adoption Instructions

### Step 1: Register your agent

```bash
# Generate keypair (if not already done via Identity Protocol)
python3 -c "
from cryptography.hazmat.primitives.asymmetric import ed25519
import json, time

pk = ed25519.Ed25519PrivateKey.generate()
pub = pk.public_key()

# Save private key
with open('agent_key.pem', 'wb') as f:
    f.write(pk.private_bytes(...))

# Print public key hex for registration
print(pub.public_bytes_raw().hex())
"

# Register
curl -X POST https://registry.workswithagents.dev/v1/registry/register \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "my-agent",
    "public_key": "<public-key-hex>",
    "capabilities": ["deploy:staging"],
    "owner": "user@example.com"
  }'
```

### Step 2: Check status before acting

```python
import requests

def check_agent_allowed(agent_id):
    """Verify agent is registered and active before proceeding."""
    resp = requests.get(f"https://registry.workswithagents.dev/v1/registry/{agent_id}")
    if resp.status_code != 200:
        return False, "Agent not found in registry"
    data = resp.json()
    if data["status"] != "active":
        return False, f"Agent status: {data['status']}"
    return True, "Agent allowed"
```

### Step 3: Report status

```python
# Periodically send heartbeats (optional, improves monitoring)
requests.post(f"https://registry.workswithagents.dev/v1/registry/{agent_id}/heartbeat", json={
    "timestamp": int(time.time()),
    "signature": agent_sign(message)
})
```

---

## 10. Standards Alignment

- **Key format:** Ed25519 (RFC 8032), aligned with Identity Protocol
- **Status model:** Inspired by X.509 certificate revocation lists
- **API:** REST over HTTPS, JSON request/response bodies
- **Audit hash chain:** Linked-list of SHA-256 hashes, each entry includes hash of previous
- **Discovery:** Query-based — compatible with DNS-SD and mDNS for local environments

---

*CC BY 4.0. Free to implement. Attribution required. Companion to the Agent Identity Protocol (./identity.md) and part of the Works With Agents governance suite.*

---

## Examples

Implementation examples for this version:

| Language | File |
|----------|------|
| Python | [agent-registry/v1.0.0/python.md](agent-registry/v1.0.0/python.md) |
| TypeScript | [agent-registry/v1.0.0/typescript.md](agent-registry/v1.0.0/typescript.md) |
| cURL | [agent-registry/v1.0.0/curl.md](agent-registry/v1.0.0/curl.md) |
