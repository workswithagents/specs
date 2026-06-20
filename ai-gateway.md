# AI Gateway / Policy Enforcement Point — Cross-Layer Governance

**Version:** 1.0.0
**Status:** Published
**Layer:** Cross-layer (L5-L7) — Agent OSI Model
**License:** CC BY 4.0

---

## 1. Purpose

A single choke point through which every agent request passes — to a model, a tool, an API, or a data store. The gateway enforces policy: who can do what, with what, how many times, and under what conditions.

Without a gateway, governance is a suggestion. The model can be prompted not to do something, but the prompt is not enforcement. The gateway is enforcement.

The AI Gateway answers: **"Is this action allowed, right now, by this agent?"**

---

## 2. Design Principles

- **Every request goes through the gateway.** No exceptions. Any agent that can bypass the gateway is not governed.
- **Policy is structured, not prompted.** Not "don't deploy to production without approval" in a system prompt. A machine-readable YAML policy that the gateway evaluates deterministically.
- **Explicit deny wins.** If any policy denies an action, it's denied. Allow is the default for unspecified actions only when the policy mode permits it.
- **Before execution, not after.** The gateway checks before the request reaches the model/tool. Blocked requests never execute.
- **Framework-agnostic.** Any agent framework can integrate. The gateway speaks REST. The agent sends requests through it.
- **Observable by design.** Every decision (allow/block/warn/throttle) is logged with the policy rule that triggered it.

---

## 3. Policy Schema

```yaml
# AI Gateway Policy
policy_version: "2.0.0"
gateway_id: "wwa-gateway-prod"
effective_date: "2026-05-26T00:00:00Z"
expires_at: null                          # null = indefinite

default_action: "deny"                    # deny | allow — default for unmatched requests

evaluation_mode: "block"                  # block | warn | log | audit-only

agents:
  - agent_id: "deploy-bot-v2"
    policy_ref: "policies/deploy-bot.yaml"
  - agent_id: "review-bot"
    policy_ref: "policies/review-bot.yaml"
  - agent_id: "*"                         # wildcard: all unlisted agents
    policy_ref: "policies/default.yaml"

# ===== Agent-Specific Policy =====
---
# policies/deploy-bot.yaml
policy_version: "2.0.0"
agent_id: "deploy-bot-v2"

permissions:
  - id: "deploy-staging"
    action: "deploy"
    target: "kubernetes:staging-cluster"
    constraint: |
      env.BRANCH == "main"
      && env.TESTS_PASS == true
      && rate("deployments", "10m") < 1
    effect: "allow"

  - id: "deploy-prod"
    action: "deploy"
    target: "kubernetes:prod-cluster"
    constraint: |
      env.BRANCH == "main"
      && env.TESTS_PASS == true
      && env.APPROVED_BY == true             # requires human approval step
      && rate("deployments", "1h") < 1
    effect: "allow"

  - id: "block-unsafe-actions"
    action: "*"
    target: "ec2:*"
    effect: "deny"                           # explicit deny — never touch EC2

  - id: "block-prod-without-approval"
    action: "deploy"
    target: "kubernetes:prod-cluster"
    constraint: "env.APPROVED_BY != true"
    effect: "deny"                           # deny if no approval

rate_limits:
  - id: "model-calls"
    action: "model_inference"
    limit: 100
    window: "1h"
    effect: "throttle"                       # slow down, don't block
    on_exceeded: "log_warning"

  - id: "deploy-frequency"
    action: "deploy"
    limit: 5
    window: "1d"
    effect: "block"
    on_exceeded: "alert_admin"

data_access:
  - id: "pii-restriction"
    dataset: "user_data"
    allowed_operations: ["read"]             # no writes to user data
    allowed_fields: ["id", "name", "email"]  # no access to sensitive fields
    constraint: "request.session_id matches active_sar"
    effect: "allow"

  - id: "block-sensitive-data"
    dataset: "user_data.health_records"
    effect: "deny"                           # no agent accesses health data

delegation:
  max_depth: 2                               # how deep can this agent delegate?
  allowed_delegates: ["build-bot", "test-bot"]
  scope_inheritance: "restrictive"           # child gets subset of parent scope

audit:
  level: "all"                               # all | decisions-only | errors-only
  include_payload: false                     # don't log request bodies (PII)
  retention_days: 365
```

---

## 4. Enforcement Modes

| Mode | Behaviour | Use Case |
|------|-----------|----------|
| **block** | Reject the request. Log the decision. Return error. | Production enforcement. The agent cannot bypass. |
| **warn** | Allow the request. Log a warning. Return success + warning header. | Gradual rollout. Let agents run while collecting data on what would be blocked. |
| **log** | Allow the request. Log the decision only. | Discovery phase. Understand what agents are doing before enforcing. |
| **audit-only** | Allow the request. Create a full attestation record. No enforcement. | Compliance environments where enforcement is handled by another system but attestation is required. |

**Migration path:** Start in `log` mode to understand agent behaviour. Move to `warn` when you've identified violations. Move to `block` when you're confident the rules are correct.

---

## 5. Gateway Architecture

```
            ┌─────────────────────────────────────┐
            │          Agent Request               │
            │  (signed, with delegation token)     │
            └──────────────┬──────────────────────┘
                           │
                           ▼
            ┌─────────────────────────────────────┐
            │         AI Gateway / PEP             │
            │                                     │
            │  1. Authenticate (verify signature)  │
            │     └── Check Registry → agent ID   │
            │                                     │
            │  2. Authorise (evaluate policy)      │
            │     └── Match action + target       │
            │     └── Evaluate constraints        │
            │     └── Check rate limits           │
            │     └── Check delegation chain      │
            │                                     │
            │  3. Route (permitted request)        │
            │     └── Model API / Tool API / Data  │
            │                                     │
            │  4. Log (every decision)             │
            │     └── Audit entry (signed)         │
            └──────────────┬──────────────────────┘
                           │
               ┌───────────┴───────────┐
               │                       │
          ALLOWED                  DENIED
               │                       │
               ▼                       ▼
         Model/Tool               Reject + Log
         Execution                 + Alert
```

### Request Flow

```
1. Agent constructs request
   {
     "intent": "deploy",
     "target": "kubernetes:staging-cluster",
     "agent_id": "deploy-bot-v2",
     "delegation_chain": [...],
     "context": {"BRANCH": "main", "TESTS_PASS": true},
     "signature": "ed25519:..."
   }

2. Gateway evaluates:
   a) Is agent_id registered?                  → Registry lookup
   b) Is signature valid?                      → Identity verification
   c) Is delegation chain valid?               → Chain verification
   d) Does action match a policy rule?         → Policy matching
   e) Are constraints satisfied?               → Expression evaluation
   f) Are rate limits within bounds?           → Counter check

3. Gateway returns:
   ALLOW → Route to execution + log
   DENY  → Return 403 with reason + log
   WARN  → Route to execution + log warning
   THROTTLE → Return 429 with retry-after + log
```

---

## 6. Policy Expression Language

Constraints use a simple expression language:

### Operators

| Operator | Example | Description |
|----------|---------|-------------|
| `==` | `env.BRANCH == "main"` | Equality (string/number) |
| `!=` | `env.ENV != "production"` | Inequality |
| `>` / `<` | `rate("calls", "1m") < 5` | Numeric comparison |
| `>=` / `<=` | `rate("calls", "1h") >= 100` | Numeric comparison |
| `matches` | `env.BRANCH matches "feature/*"` | Regex match |
| `in` | `env.TARGET in ["staging", "dev"]` | Set membership |
| `and` | `cond1 and cond2` | Logical AND |
| `or` | `cond1 or cond2` | Logical OR |
| `not` | `not env.IS_FORK` | Logical NOT |

### Built-in Functions

| Function | Description |
|----------|-------------|
| `rate(name, window)` | Request count in time window (e.g., `rate("deployments", "10m")`) |
| `now()` | Current timestamp |
| `has_permission(agent, action, target)` | Check if agent has a permission |
| `is_delegated_from(agent_id)` | Check delegation chain origin |

---

## 7. API

### Evaluate Request

```http
POST /v1/gateway/evaluate
Content-Type: application/json

{
  "agent_id": "deploy-bot-v2",
  "intent": "deploy",
  "target": "kubernetes:staging-cluster",
  "context": {
    "BRANCH": "main",
    "TESTS_PASS": true
  },
  "delegation_chain": [
    {"agent_id": "human-vilius", "scope": {"action": ["deploy:staging"]}, "sig": "..."},
    {"agent_id": "orchestrator", "scope": {"action": ["deploy:staging"]}, "sig": "..."}
  ],
  "signature": "ed25519:agent_signed_request..."
}

→ 200 OK (ALLOW)
{
  "decision": "allow",
  "decision_id": "gwy-dec-a1b2c3",
  "matched_rules": [
    {
      "rule_id": "deploy-staging",
      "effect": "allow",
      "constraint_evaluation": {"BRANCH": true, "TESTS_PASS": true, "rate": true}
    }
  ],
  "remaining_rate_limits": {
    "deployments_10m": 0,
    "deployments_1d": 4
  }
}

→ 200 OK (DENY)
{
  "decision": "deny",
  "decision_id": "gwy-dec-d4e5f6",
  "reason": "Rate limit exceeded: deployments per 10m (limit 1, current 1)",
  "matched_rules": [
    {
      "rule_id": "deploy-staging",
      "effect": "deny",
      "constraint_evaluation": {"BRANCH": true, "TESTS_PASS": true, "rate": false}
    }
  ],
  "retry_after": "2026-05-26T12:10:00Z"
}
```

### Health Check

```http
GET /v1/gateway/health

→ 200 OK
{
  "status": "healthy",
  "policies_loaded": 12,
  "agents_registered": 8,
  "requests_24h": 1432,
  "allowed_24h": 1388,
  "denied_24h": 44,
  "avg_evaluation_ms": 3.2
}
```

---

## 8. Integration with Agent Registry

The gateway depends on the registry for authentication:

```
Gateway Request
    │
    ├── GET /v1/registry/{agent_id}
    │   Returns: agent status, public key, capabilities
    │   → If status != active: DENY
    │
    ├── Verify request signature against registered public key
    │   → If signature invalid: DENY
    │
    ├── Evaluate policy (see Section 5)
    │
    └── Log decision
```

An agent that isn't registered cannot reach the policy evaluation stage — it's denied at authentication.

---

## 9. Integration with Delegation Framework

When a delegation chain is present in the request, the gateway:

1. Walks the chain from leaf to root
2. Verifies each delegation token's signature
3. Checks each token's scope covers the requested action
4. Confirms no token has expired
5. Computes the effective scope (intersection of all scopes in chain)
6. Applies the effective scope as a constraint on the policy evaluation

If any token is invalid, expired, or insufficiently scoped → DENY.

---

## 10. Threat Model

| Threat | Protection |
|--------|-----------|
| **Bypass gateway** (agent calls model/tool directly) | Network-layer enforcement: only the gateway has credentials for model/tool APIs. Agents must route through it. |
| **Policy tampering** (unauthorised policy change) | Policy files are signed. Gateway verifies signature on load. Unauthorised changes are detected on next reload. |
| **Rate limit exhaustion** (agent spams allowed actions) | Per-agent + per-action rate limits. Exceeded → throttle → block. Configurable alert thresholds. |
| **Delegation abuse** (action claimed under invalid delegation) | Gateway verifies every delegation token. Expired, revoked, or insufficiently scoped tokens are rejected. |
| **Prompt injection through gateway** (malicious input in request context) | Gateway evaluates context fields as typed expressions, not strings. Injection attempt → type mismatch → constraint failure → DENY. |
| **Replay attack** (intercepted request replayed) | Timestamp + nonce in every request. Requests older than 60s rejected. Nonce tracked for dedup. |

---

## 11. Deployment Patterns

### Sidecar Gateway
A local process that intercepts all agent → model/tool calls. Simple, zero network dependencies. Good for single-agent setups and development.

### Centralised Gateway
A shared service that all agents in an organisation route through. Single policy store, unified audit log. Good for teams and regulated environments.

### Hybrid
Local sidecar for performance (cached policies, low latency), central gateway for audit and cross-team coordination. Sidecar syncs decisions to central store asynchronously.

---

## 12. Agent Adoption Instructions

### Step 1: Route through the gateway

```python
import requests

def call_model_via_gateway(agent_id, model, prompt, delegation_chain):
    """Make an authorised model call through the AI Gateway."""
    response = requests.post(
        "https://gateway.internal/v1/gateway/evaluate",
        json={
            "agent_id": agent_id,
            "intent": "model_inference",
            "target": f"model:{model}",
            "context": {"tokens": len(prompt)},
            "delegation_chain": delegation_chain,
            "signature": sign_message(...)
        }
    )
    data = response.json()
    if data["decision"] == "deny":
        raise PermissionError(f"Gateway denied: {data['reason']}")

    # Gateway approved — proceed to model
    return call_model_directly(model, prompt)
```

### Step 2: Handle denials gracefully

```python
def safe_call(agent_id, intent, target, context):
    response = gateway_evaluate(agent_id, intent, target, context)
    if response["decision"] == "deny":
        if "rate limit" in response.get("reason", "").lower():
            wait_until = response.get("retry_after")
            logger.info(f"Rate limited until {wait_until}, backing off")
            return None, "rate_limited"
        elif "permission" in response.get("reason", "").lower():
            logger.warning(f"Permission denied: {response['reason']}")
            return None, "denied"
        else:
            logger.error(f"Unexpected denial: {response['reason']}")
            return None, "error"
    return execute(intent, target, context), "allowed"
```

### Step 3: Verify gateway is active

```bash
# Check gateway health and policy stats
curl -s https://gateway.internal/v1/gateway/health | jq
{
  "status": "healthy",
  "policies_loaded": 12,
  "agents_registered": 8,
  "denied_24h": 44
}
```

---

## 13. Standards Alignment

- **Policy format:** YAML — human-readable, machine-enforceable
- **Expressions:** Simple DSL (NO JavaScript, NO Python — prevents injection)
- **Authentication:** Ed25519 (RFC 8032), aligned with Identity Protocol
- **Transport:** HTTPS — TLS 1.3 minimum
- **Audit:** Signed audit entries, SHA-256 hash chain
- **Rate limiting:** Sliding window counters (token bucket compatible)

---

*CC BY 4.0. Free to implement. Attribution required. Companion to the Agent Registry (./agent-registry.md) and Delegation Framework (./delegation-framework.md). Part of the Works With Agents governance suite.*
