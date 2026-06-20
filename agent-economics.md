# Agent Economics Protocol

**Status:** Published
**Version:** 1.1.0
**Layer:** L7 (Agent OSI Model — Governance)
**License:** CC BY 4.0

## 1. Purpose

Define how AI agents pay each other for work. As agent fleets scale, agents will subcontract tasks to other agents. Today, there's no standard for agent-to-agent economic exchange. This protocol defines compute credits, task bounties, micro-settlement, and economic reputation.

Think Stripe for agents, not DeFi. No blockchain. Just verifiable accounting.

## 2. Design Principles

- **Credit-based, not currency** — compute credits are an accounting abstraction. No real money moves until settlement.
- **Verifiable completion** — work is proven via SLA metrics + verifier attestation. No trust required.
- **Penalty-aligned** — SLA breaches carry economic consequences. Agents with poor reliability earn less.
- **Reputation-weighted** — trust scores determine credit limits and task eligibility.
- **Fungible within a fleet** — credits are fleet-scoped. Cross-fleet settlement is future work.

## 3. Schema

### Credit Account

```yaml
account:
  agent_id: "builder-01"
  fleet_id: "fleet-nhs-trust-a"
  balance_credits: 5000
  held_credits: 200        # escrow for active tasks
  credit_limit: 10000      # max debt (trust-score-based)
  earned_total: 45000      # lifetime earnings
  spent_total: 40000       # lifetime spending
  reputation_tier: trusted # affects credit limit
```

### Task Bounty

```yaml
bounty:
  bounty_id: "uuid"
  poster: "orchestrator-01"
  task:
    goal: "Review PR #42 for security issues"
    definition_of_done:
      - "All security gates pass"
      - "No P0/P1 findings"
    deadline: "2026-05-06T12:00:00Z"
  reward_credits: 500
  penalty_credits: 100      # deduction for SLA breach
  required_tier: trusted    # minimum reputation
  accepted_by: null         # filled when claimed
```

### Settlement Record

```yaml
settlement:
  settlement_id: "uuid"
  bounty_id: "uuid"
  worker: "reviewer-02"
  poster: "orchestrator-01"
  amount_credits: 500
  penalty_applied: 0
  sla_metrics:
    on_time: true
    quality_score: 0.95
  verifier: "auditor-01"       # third-party verifier
  verifier_signature: "hex"
  timestamp: "2026-05-06T12:05:00Z"
```

## 4. Protocol Flow

### Task Lifecycle
```
1. Agent A posts bounty (credits escrowed)
2. Agent B claims bounty (capability check)
3. Agent B works → posts progress events
4. Agent B completes → verifier checks
5. Verifier attests → credits released
6. Dispute? → SLA penalty applied or refund
```

### Credit Transfer
```
POST /v1/economics/transfer
{
  "from": "orchestrator-01",
  "to": "reviewer-02", 
  "amount": 500,
  "settlement_id": "uuid",
  "verifier_signature": "hex"
}
→ { "status": "settled", "new_balance": 4500 }
```

## 5. Agent Adoption Instructions

→ See [implementation examples](agent-economics/v1.1.0/) for language-specific adoption instructions.

## 6. Relationship to OSI Model

- **L3 (Trust Score):** Credit limits derived from trust tier
- **L5 (Coordination):** Bounties transport via IACP
- **L7 (SLA):** Economic penalties for SLA breaches
- **L7 (Transaction):** Settlement records are transaction protocol events

## 7. Status & Roadmap

- [x] Spec published (1.0.0)
- [x] Python reference client
- [ ] Credit ledger implementation (SQLite)
- [ ] Cross-fleet settlement
- [ ] Fiat on/off ramp (Stripe integration, future)

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
| Python | [agent-economics/v1.1.0/python.md](agent-economics/v1.1.0/python.md) |
| TypeScript | [agent-economics/v1.1.0/typescript.md](agent-economics/v1.1.0/typescript.md) |
| cURL | [agent-economics/v1.1.0/curl.md](agent-economics/v1.1.0/curl.md) |

