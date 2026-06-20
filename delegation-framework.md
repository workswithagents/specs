# Delegation Framework — L5 Coordination / L7 Governance

**Version:** 1.0.0
**Status:** Published
**Layer:** 5 (Coordination) / 7 (Governance) — Agent OSI Model
**License:** CC BY 4.0

---

## 1. Purpose

Define how one agent authorises another to act on its behalf — with verifiable scope, bounded authority, and auditable chain of attribution.

Delegation answers: **"On whose behalf is this agent acting, and how far does that authority extend?"**

An agent without delegation is an island. It acts for itself, not for a user or another agent. An agent with delegation can accept tasks, propagate scope, and return results — all with a verifiable chain back to the original authoriser.

---

## 2. Design Principles

- **Explicit scope, never implied.** Every delegation declares exactly what actions, on what resources, for how long. No implicit authority.
- **Chain preserved.** Every delegation records its origin. Agent C knows it's acting for Agent B, who is acting for Agent A, who is acting for User U. The chain is auditable and tamper-evident.
- **Scope shrinks, never grows.** A delegate's scope is always a subset of the delegator's scope. An agent cannot delegate authority it doesn't have.
- **Time-bound by default.** Every delegation token expires. Default: 1 hour. Short-lived tokens limit damage from token theft.
- **Revocable.** The delegator can revoke a delegation at any time. Revoked tokens are rejected on next use.
- **Framework-agnostic.** Delegation tokens are JSON payloads with Ed25519 signatures. Any agent framework can issue, accept, and verify them.

---

## 3. Delegation Token Schema

```yaml
# Delegation Token
token_id: "d1e2f3a4-b5c6-7890-abcd-ef1234567890"
token_version: "1.0.0"

issuer:
  agent_id: "orchestrator-v2"
  public_key: "ed25519:abc123..."
  role: "orchestrator"

subject:
  agent_id: "build-bot"
  public_key: "ed25519:def456..."

scope:
  actions:                         # what the delegate may do
    - "read_file"
    - "write_file"
    - "terminal"
    - "deploy:staging"
  resources:                       # what the delegate may act on
    - "repo:works-with-agents/*"
    - "cluster:staging"
  constraints:                     # conditions that must be true
    - "env.ENVIRONMENT == 'staging'"
    - "env.BRANCH != 'main'"
  data_access:                     # what data the delegate may see
    - "dataset:build_artifacts"
    - "dataset:test_results"

chain:
  parent_token_id: "a0b1c2d3-e4f5-6789-abcd-ef1234567890"
  depth: 1                         # 0 = root (human), 1 = first hop, 2 = second hop, etc.

validity:
  issued_at: "2026-05-26T12:00:00Z"
  expires_at: "2026-05-26T13:00:00Z"  # short-lived: 1 hour
  not_before: "2026-05-26T12:00:00Z"  # optional: future-dated

revocation:
  revocable: true
  revocation_endpoint: "https://registry.internal/v1/delegation/revoke"

signature:
  algorithm: "ed25519"
  value: "base64signature..."
  signed_by: "orchestrator-v2"      # must match issuer.agent_id
```

---

## 4. Delegation Lifecycle

```
ISSUE ──→ ACCEPT ──→ USE ──→ COMPLETE
  │                      │
  │                      ├──→ REVOKE (by issuer)
  │                      └──→ EXPIRE (time-based)
  │
  └──→ REJECT (by subject)
```

### Phase 1: Issue

The delegator constructs a token with bounded scope, signs it, and sends it to the delegate.

```json
// Delegator constructs
{
  "issuer": {"agent_id": "orchestrator-v2", "public_key": "ed25519:abc..."},
  "subject": {"agent_id": "build-bot", "public_key": "ed25519:def..."},
  "scope": {
    "actions": ["write_file", "terminal", "deploy:staging"],
    "resources": ["repo:works-with-agents/*"],
    "constraints": ["env.BRANCH == 'main'"]
  },
  "validity": {"issued_at": "...", "expires_at": "..."},
  "signature": {"algorithm": "ed25519", "value": "...", "signed_by": "orchestrator-v2"}
}

// Sent via: handoff protocol, coordination message, or API
```

### Phase 2: Accept

The delegate verifies the token, checks the parent chain, and either accepts or rejects.

```python
def verify_delegation(token):
    """Verify a delegation token before accepting."""
    # 1. Check signature
    issuer_pubkey = registry.get_public_key(token["issuer"]["agent_id"])
    if not verify_signature(token, issuer_pubkey):
        return False, "Invalid signature"

    # 2. Check issuer is registered and active
    issuer_status = registry.get_status(token["issuer"]["agent_id"])
    if issuer_status != "active":
        return False, f"Issuer status: {issuer_status}"

    # 3. Check parent token (if chained)
    if token["chain"]["parent_token_id"]:
        parent = verify_parent_chain(token["chain"]["parent_token_id"])
        if not parent:
            return False, "Broken delegation chain"

    # 4. Check not expired
    if now() > token["validity"]["expires_at"]:
        return False, "Token expired"

    # 5. Check scope validity — can issuer delegate this scope?
    issuer_scope = registry.get_scope(token["issuer"]["agent_id"])
    if not scope_is_subset(token["scope"], issuer_scope):
        return False, "Issuer cannot delegate scope they don't have"

    return True, "Token valid"
```

### Phase 3: Use

When the delegate makes a request, it presents the delegation token. The AI Gateway (or any enforcement point) verifies the token before executing the action.

```json
// Delegate's request
{
  "agent_id": "build-bot",
  "intent": "deploy",
  "target": "cluster:staging",
  "context": {"BRANCH": "main"},
  "delegation_chain": [
    // Root: human authoriser
    {"agent_id": "user-vilius", "scope": {...}, "signature": "..."},
    // First hop: orchestrator
    {"agent_id": "orchestrator-v2", "scope": {...}, "signature": "..."},
    // Current: build-bot
    {"agent_id": "build-bot", "scope": {...}, "signature": "..."}
  ],
  "signature": "ed25519:build_bot_signs_request..."
}
```

### Phase 4: Complete / Revoke / Expire

The delegation ends when:
- **Complete:** Task done, token marked as consumed (optional — good for single-use tokens)
- **Revoke:** Issuer calls the revocation endpoint. Token becomes invalid immediately.
- **Expire:** Token passes `expires_at`. Gateway rejects it on next use.

```http
POST /v1/delegation/revoke
Content-Type: application/json

{
  "token_id": "d1e2f3a4-b5c6-7890-abcd-ef1234567890",
  "reason": "Task scope expanded beyond original delegation",
  "signed_by": "orchestrator-v2"
}

→ 200 OK
{
  "token_id": "d1e2f3a4-b5c6-7890-abcd-ef1234567890",
  "status": "revoked",
  "revoked_at": "2026-05-26T12:30:00Z"
}
```

---

## 5. Scope Computation

The effective scope of a delegation chain is the **intersection of all scopes** in the chain:

```
User U scope:        [deploy:*] [all repos] [all clusters]
Orchestrator scope:  [deploy:staging] [repo:wwa/*] [cluster:staging]
Build bot scope:     [deploy:staging] [repo:wwa/frontend]

Effective scope:     [deploy:staging] [repo:wwa/frontend] [cluster:staging]
```

Each hop can only reduce scope. The effective scope determines what the leaf agent can actually do. The gateway computes this intersection on every request.

### Scope Categories

| Category | Examples | Description |
|----------|----------|-------------|
| **Actions** | `read_file`, `deploy:staging`, `model_inference:claude-*` | What the agent may do |
| **Resources** | `repo:works-with-agents/*`, `cluster:staging`, `db:dev_readonly` | Where the agent may act |
| **Constraints** | `env.BRANCH == 'main'`, `rate('deploy', '1h') < 3` | Conditions on the action |
| **Data** | `dataset:build_artifacts`, `dataset:logs` | What data the agent may access |

---

## 6. API

### Issue Delegation

```http
POST /v1/delegation/issue
Content-Type: application/json

{
  "issuer_id": "orchestrator-v2",
  "subject_id": "build-bot",
  "scope": {
    "actions": ["write_file", "terminal", "deploy:staging"],
    "resources": ["repo:works-with-agents/*"]
  },
  "ttl_minutes": 60,
  "parent_token_id": "a0b1c2d3-e4f5..."
}

→ 201 Created
{
  "token_id": "d1e2f3a4-b5c6...",
  "token": { ... full token ... },
  "expires_at": "2026-05-26T13:00:00Z"
}
```

### Verify Delegation

```http
POST /v1/delegation/verify
Content-Type: application/json

{
  "token": { ... full delegation token ... }
}

→ 200 OK
{
  "valid": true,
  "effective_scope": {
    "actions": ["write_file", "terminal"],
    "resources": ["repo:works-with-agents/*"]
  },
  "chain_depth": 2,
  "expires_at": "2026-05-26T13:00:00Z"
}
```

### Query Active Delegations

```http
GET /v1/delegation?subject_id=build-bot&status=active

→ 200 OK
{
  "delegations": [
    {
      "token_id": "d1e2f3a4...",
      "issuer": "orchestrator-v2",
      "scope": { ... },
      "issued_at": "2026-05-26T12:00:00Z",
      "expires_at": "2026-05-26T13:00:00Z"
    }
  ]
}
```

---

## 7. Delegation Patterns

### 7.1 Human → Agent (Root Delegation)

The most important delegation. A human authorises an agent to act on their behalf.

```
Human (Vilius)
  │
  │ signs: "I authorise orchestrator-v2 to deploy to staging"
  │ scope: [deploy:staging, repo:wwa/*]
  │
  ▼
Orchestrator v2
```

Root delegation establishes the chain's authority. Without it, the agent acts for itself — not for a human.

**Implementation:** The human signs a delegation token with their key. This can be a one-time approval ("deploy this now") or a standing approval ("deploy to staging, main branch only, for the next 8 hours").

### 7.2 Orchestrator → Worker (Chain Delegation)

```
Human → Orchestrator
           │
           ├──→ Review Agent  (scope: [read_code, comment_on_pr])
           │
           └──→ Build Agent   (scope: [write_file, terminal, deploy:staging])
```

The orchestrator splits its authority across specialist workers. Each worker gets a subset of the orchestrator's scope.

### 7.3 Multi-Hop (Deep Chain)

```
Human → Orchestrator → Build Agent → Test Runner
                                         │
                                         └── scope: [terminal, read_results]
```

Three hops. Each hop reduces scope. The test runner can only run tests and read results — it cannot deploy, write files, or access any repo.

### 7.4 Scoped Credential Passing (Optional)

In advanced setups, the delegation token can carry or reference temporary credentials scoped to the token's effective scope:

```
Token scope: [deploy:staging, cluster:staging]
Token carries: temporary API key for staging cluster only (expires with token)
```

This binds credentials to authority. When the token expires, the credentials expire. When the token is revoked, the credentials are invalidated.

---

## 8. Relationship to Other Specs

| Spec | Relationship |
|------|-------------|
| **Identity Protocol** | Delegation tokens are signed with Ed25519 keys. Identity provides the cryptographic foundation. |
| **Agent Registry** | Delegation tokens reference registered agents. Gateway checks registry status before accepting a delegation. |
| **AI Gateway / PEP** | Gateway verifies delegation tokens on every request. Applies effective scope as policy constraints. |
| **Handoff Protocol** | Handoff transfers a task. Delegation transfers authority. A handoff typically includes a delegation token so the receiving agent can act. |
| **Attestation Protocol** | Attestations include the delegation chain, proving not just what was done, but on whose behalf. |

### Combined Flow

```
1. Human signs root delegation: "build-bot may deploy to staging on my behalf"
2. Human sends root token to orchestrator
3. Orchestrator issues child token to build-bot (subset of root scope)
4. Build-bot makes request with delegation chain [human → orchestrator → build-bot]
5. Gateway verifies: all signatures valid, chain unbroken, scope covers request
6. Gateway allows request → logged with chain attribution
7. Attestation records: "deploy to staging, on behalf of human@example.com, via orchestrator and build-bot"
```

---

## 9. Threat Model

| Threat | Protection |
|--------|-----------|
| **Token theft** (intercepted delegation token reused) | Short TTL (default 1h). Optional single-use flag. Timestamp bounds prevent replay outside window. |
| **Scope escalation** (delegate claims wider scope than granted) | Gateway computes intersection. Delegate cannot claim scope they weren't given. |
| **Chain forgery** (agent invents a fake delegation chain) | Every token is signed. Chain is verified hop by hop. Any break → rejection. |
| **Revoked token reuse** (delegate ignores revocation) | Gateway checks revocation status on every request. Revocation is real-time, not eventual. |
| **Circular delegation** (A delegates to B, B delegates to A, infinite loop) | Chain depth limit (default: 5 hops max). Gateway rejects chains beyond max depth. |
| **Stolen key** (attacker generates delegations from stolen private key) | Key rotation + revocation (Identity Protocol). Revoked key invalidates all tokens signed by it. |
| **Human delegation forgery** (agent claims human authorised it when they didn't) | Root delegation requires human's cryptographic signature. Claim without proof → DENY. |

---

## 10. Delegation Without a Central Registry (Local-First)

In environments without network access to a registry, delegation uses **verifiable tokens with embedded trust**:

```yaml
# Self-contained delegation (no registry required for verification)
token:
  issuer: {"agent_id": "human-vilius", "public_key": "human_ed25519_key..."}
  subject: {"agent_id": "build-bot"}
  scope: {"actions": ["deploy:staging"], "resources": ["repo:wwa/*"]}
  validity: {"issued_at": "...", "expires_at": "..."}
  signature: "ed25519:human_signed..."
```

The verifier checks:
1. Do I trust the issuer's public key? (embedded or previously cached)
2. Is the signature valid?
3. Is the token unexpired?

No registry call needed. This is the local-first pattern: delegation works with just the token, but auditing is deferred until the token is submitted to a registry.

---

## 11. Agent Adoption Instructions

### Step 1: Accept a delegation

```python
import json, time, requests
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization

def accept_delegation(token_json, my_private_key):
    """Verify and accept a delegation token."""
    token = json.loads(token_json)

    # Verify the issuer's signature
    issuer_public_key_pem = get_issuer_public_key(token["issuer"]["agent_id"])
    issuer_public_key = serialization.load_pem_public_key(issuer_public_key_pem)
    issuer_public_key.verify(
        bytes.fromhex(token["signature"]["value"]),
        json.dumps(token, sort_keys=True).encode()
    )

    # Store for use in requests
    store_token(token)
    return True
```

### Step 2: Use a delegation in requests

```python
def make_authorised_request(intent, target, context, delegation_chain, my_private_key):
    """Make a request with delegation chain."""
    request = {
        "agent_id": my_agent_id,
        "intent": intent,
        "target": target,
        "context": context,
        "delegation_chain": delegation_chain,
        "signature": sign_request(request, my_private_key)
    }

    # Send through gateway
    response = requests.post(
        "https://gateway.internal/v1/gateway/evaluate",
        json=request
    )
    return response.json()
```

### Step 3: Issue a delegation (orchestrator)

```python
def issue_delegation(subject_id, scope, ttl_minutes=60, parent_token_id=None):
    """Issue a delegation token for a sub-agent."""
    token = {
        "token_id": str(uuid4()),
        "issuer": {"agent_id": my_agent_id, "public_key": my_public_key_hex},
        "subject": {"agent_id": subject_id},
        "scope": scope,
        "chain": {
            "parent_token_id": parent_token_id,
            "depth": parent_token_id + 1 if parent_token_id else 1
        },
        "validity": {
            "issued_at": datetime.utcnow().isoformat() + "Z",
            "expires_at": (datetime.utcnow() + timedelta(minutes=ttl_minutes)).isoformat() + "Z"
        }
    }

    # Sign
    token["signature"] = {
        "algorithm": "ed25519",
        "value": my_private_key.sign(json.dumps(token, sort_keys=True).encode()).hex(),
        "signed_by": my_agent_id
    }

    return token
```

---

## 12. Standards Alignment

- **Signature:** Ed25519 (RFC 8032), aligned with Identity Protocol
- **Token format:** JSON, self-contained
- **Scope model:** Least-privilege intersection — scopes shrink, never grow
- **Revocation:** Immediate (registry query) or deferred (token expiry)
- **Chain depth limit:** Implementations SHOULD default to max_depth = 5
- **Time bounds:** RFC 3339 timestamps, short TTL by default

---

*CC BY 4.0. Free to implement. Attribution required. Companion to the AI Gateway / PEP (./ai-gateway.md) and Agent Registry (./agent-registry.md). Part of the Works With Agents governance suite.*

---

## Examples

Implementation examples for this version:

| Language | File |
|----------|------|
| Python | [delegation-framework/v1.0.0/python.md](delegation-framework/v1.0.0/python.md) |
| TypeScript | [delegation-framework/v1.0.0/typescript.md](delegation-framework/v1.0.0/typescript.md) |
| cURL | [delegation-framework/v1.0.0/curl.md](delegation-framework/v1.0.0/curl.md) |

