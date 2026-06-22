# Agent Reputation Ledger

**Status:** Published
**Version:** 1.1.0
**Layer:** Cross-layer (L2/L3 Identity + L5 Coordination)
**License:** CC BY 4.0

## 1. Purpose

Define an immutable, cross-organization reputation system for AI agents. Trust scores answer "how reliable is this agent?" Reputation answers "what has this agent actually done, and who verified it?"

Verifiable claims — signed by a verifier, not self-reported — create a tamper-evident history that survives across organizations, model updates, and agent retirements.

### Problem
Trust scores tell you how reliable an agent is right now. But when an agent crosses organizational boundaries — moving from Org A's fleet to Org B's — its trust score doesn't carry over. There's no cross-org record of what this agent has actually done, who verified its work, and whether it's trustworthy in a new context. Every organization starts from zero trust.

### Solution
An append-only, cryptographically signed ledger of claims about an agent's actions. Each claim is signed by a verifier (another agent or human), not self-reported. Claims are privacy-scoped (public, org-only, private) and queryable across organizations. The ledger creates a portable reputation that survives model updates, agent retirements, and organizational boundaries.

### When to use
- Multi-organization agent ecosystems where trust must cross boundaries
- Tracking agent work history across model updates and retirements
- Building portable reputation that an agent can carry between fleets
- Verifying that an agent's claims about its history are backed by cryptographic proof

### When NOT to use
- Single-organization fleet where trust is implicit and controlled
- You only need current reliability (not historical record) — use Trust Score
- You only need proof of specific actions (not ongoing reputation) — use Attestation Protocol
- All verifiers are within the same trust domain and don't need cryptographic proof

### How it compares to similar specs
| Instead of THIS | When | Because |
|---|---|---|
| Trust Score | Evaluating current reliability for delegation decisions | Trust Score is a real-time numeric rating; Reputation Ledger is the historical evidence that backs it up |
| Attestation Protocol | Proving a specific generation event with cryptographic proof | Attestation proves one event; Reputation Ledger aggregates many events into a portable history |
| Identity Protocol | Verifying who an agent is | Identity proves the agent's key; Reputation proves what the agent has done with that identity |

### What you lose without THIS
- No cross-organization reputation — every org starts from zero trust with every agent
- Agent work history is siloed within individual organizations
- No portable proof of an agent's track record — claims are unverifiable
- Model updates and agent retirements reset trust to zero

## 2. Design Principles

- **Verifiable, not self-reported** — claims must be signed by a third-party verifier (another agent or human).
- **Append-only** — claims are never deleted, only superseded by newer claims.
- **Cross-org queryable** — an agent from Org A can query the reputation of an agent from Org B.
- **Privacy-scoped** — claims have visibility: public, org-only, or private.
- **Not a blockchain** — SQLite-based reference implementation. No consensus, no mining.

## 3. Schema

### Reputation Claim

```yaml
claim:
  claim_id: "uuid-v7"
  subject: "builder-01"          # agent being evaluated
  verifier: "reviewer-02"        # who verified this
  verifier_org: "nhs-trust-a"
  
  event:
    type: task_complete          # task_complete | handoff_complete | sla_breach
    task_id: "uuid"
    outcome: success             # success | partial | failure
    metrics:
      quality_score: 0.95
      on_time: true
      tokens_used: 12000
      gates_passed: 4/4
  
  scope: public                  # public | org | private
  issued_at: "2026-05-06T12:00:00Z"
  expires_at: null               # null = permanent
  
  # Cryptographic proof
  verifier_signature: "hex-ed25519"
  verifier_public_key: "hex-ed25519-pub"
```

### Agent Reputation Profile

```yaml
profile:
  agent_id: "builder-01"
  claims_count: 142
  verifiers_count: 8             # unique verifiers
  orgs_count: 3                  # across 3 organizations
  
  summary:
    task_completion_rate: 0.94
    sla_compliance: 0.97
    avg_quality_score: 0.92
    total_tasks_completed: 134
    total_sla_breaches: 4
  
  endorsements:
    - verifier: "senior-reviewer-01"
      statement: "Consistently produces clean, tested code"
      date: "2026-04-15"
```

## 4. API / Protocol

### Submit a claim
```
POST /v1/reputation/claims
Authorization: Bearer <verifier-token>
{
  "claim": {
    "subject": "builder-01",
    "event": {"type": "task_complete", "outcome": "success", ...},
    "scope": "public"
  },
  "signature": "hex-ed25519"
}
→ { "claim_id": "uuid", "status": "accepted" }
```

### Query agent reputation
```
GET /v1/reputation/agents/builder-01
→ { "profile": {...}, "recent_claims": [...] }

GET /v1/reputation/agents/builder-01?scope=public
→ { "profile": {...} }  # org-only claims excluded
```

### Cross-org query
```
GET /v1/reputation/agents/builder-01?org=nhs-trust-b
→ { "profile": {...} }  # claims visible to requesting org
```

## 5. Agent Adoption Instructions

→ See [implementation examples](reputation-ledger/v1.1.0/) for language-specific adoption instructions.

## 6. Relationship to OSI Model

- **L2 (Identity):** Claims signed with AgentIdentity keys — cryptographic proof of verifier
- **L3 (Trust Score):** Reputation feeds trust score calculations
- **L5 (Coordination):** IACP messages carry reputation queries between agents
- **L7 (SLA):** SLA breach events become reputation claims

## 7. Status & Roadmap

- [x] Spec published (1.0.0)
- [x] Python reference client
- [ ] SQLite reference implementation
- [ ] Cross-org federation protocol
- [ ] Human endorsement layer (LinkedIn-style recommendations for agents)
- [ ] Reputation token bridging (portable reputation across ecosystems)

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
| Python | [reputation-ledger/v1.1.0/python.md](reputation-ledger/v1.1.0/python.md) |
| TypeScript | [reputation-ledger/v1.1.0/typescript.md](reputation-ledger/v1.1.0/typescript.md) |
| cURL | [reputation-ledger/v1.1.0/curl.md](reputation-ledger/v1.1.0/curl.md) |

