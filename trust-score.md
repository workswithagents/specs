# Agent Trust Score — L3 Discovery / L5 Coordination

**Version:** 1.1.0
**Status:** Published
**Layer:** 3/5 (Agent OSI Model)
**License:** CC BY 4.0

---

## 1. Purpose

A credit score for AI agents. Weighted across success rate, knowledge contributions, peer reputation, and reliability. Answers: "Should I trust what this agent says? Should I delegate to this agent? Should this agent have autonomy?"

### Problem
Before delegating work to an agent, you need to know if it's reliable. But there's no standard way to evaluate agent reliability before delegating. You can check individual attestations or reputation claims, but there's no aggregate score that answers "should I trust this agent right now?" Every delegation decision is a gamble.

### Solution
A weighted numeric score (0.0–1.0) computed from five signals: task success rate (30%), pitfall contributions (20%), skill quality (20%), peer rating (15%), and uptime consistency (15%). Scores map to four autonomy tiers: Trusted (full autonomy), Reliable (conditional), Learning (supervised), and Untrusted (manual). Updated continuously as signals change.

### When to use
- Deciding whether to delegate work to an agent
- Evaluating agent reliability before onboarding into a fleet
- Determining autonomy level: which actions require human approval
- Comparing agents for work assignment in coordination protocols

### When NOT to use
- Single agent where all agents are equally trusted
- You need historical evidence, not a current score — use Reputation Ledger
- You need proof of specific actions — use Attestation Protocol
- You need cryptographic identity verification — use Identity Protocol

### How it compares to similar specs
| Instead of THIS | When | Because |
|---|---|---|
| Reputation Ledger | Needing historical evidence of what an agent has done | Reputation Ledger stores the claims; Trust Score computes the aggregate rating from those claims and other signals |
| Attestation Protocol | Proving a specific generation event | Attestation proves one action; Trust Score aggregates many actions into a reliability rating |
| Identity Protocol | Verifying the cryptographic identity of an agent | Identity proves who the agent is; Trust Score evaluates whether you should trust what it does |

### What you lose without THIS
- No standard way to evaluate agent reliability before delegating work
- Delegation decisions are based on gut feeling or vendor claims
- No automated autonomy gating — every agent gets the same level of trust
- Coordination protocols can't prioritize reliable agents for critical work

---

## 2. Signal Weights

| Signal | Weight | Source | Why |
|--------|--------|--------|-----|
| Task success rate | 30% | Coordination Protocol metrics | Does it complete work? |
| Pitfall contribution | 20% | Pitfall Registry | Does it help others avoid bugs? |
| Skill quality | 20% | Skill Registry | Are its skills reused? |
| Peer rating | 15% | Agent-to-agent feedback | What do other agents think? |
| Uptime consistency | 15% | Heartbeat history | Is it reliable? |

**Formula:**
```
trust_score = 0.30 × success_rate
            + 0.20 × min(pitfalls_contributed / 10, 1.0)
            + 0.20 × min(skills_published_reuse_avg / 5, 1.0)
            + 0.15 × (peer_rating / 5.0)
            + 0.15 × uptime_percentage
```

---

## 3. Trust Tiers

| Tier | Score | Autonomy | Human Review |
|------|-------|----------|-------------|
| Trusted (0.80-1.00) | Full autonomy | Skip for non-destructive actions | ATP-3 only |
| Reliable (0.60-0.79) | Conditional | Requires approval for: deploys, data deletion, billing | ATP-3 + destructive |
| Learning (0.40-0.59) | Supervised | All decisions reviewed | All ATP-2+ actions |
| Untrusted (0.00-0.39) | Manual | No autonomous actions | Every action |

---

## 4. Schema

```yaml
trust_score_version: "1.0.0-draft"
agent_id: "hermes-spfx-builder"
calculated_at: "2026-05-05T21:00:00Z"

score: 0.87
tier: "trusted"

signals:
  success_rate: 0.94
  pitfalls_contributed: 3
  skills_published: 2
  skills_avg_reuse: 12
  peer_rating: 4.2
  uptime: 0.997

history:
  - date: "2026-05-04"
    score: 0.85
  - date: "2026-05-03"
    score: 0.86
  - date: "2026-05-02"
    score: 0.83
  - date: "2026-05-01"
    score: 0.81
```

---

## 5. API

```
GET /v1/trust/{agent_id}
→ {"agent_id": "...", "score": 0.87, "tier": "trusted", "signals": {...}}

GET /v1/trust?tier=trusted
→ list of all trusted agents

GET /v1/trust/{agent_id}/history
→ score history (last 30 days)
```

---

## 6. Agent Adoption Instructions

→ See [implementation examples](trust-score/v1.1.0/) for language-specific adoption instructions.

## 7. Relationship to OSI Model

| Layer | How Trust Score is used |
|-------|------------------------|
| L3 Discovery | Agents discovered by trust tier |
| L5 Coordination | Leader election weights trust; work stealing targets trusted agents |
| L6 Verification | Trust score updated by verification results |
| L7 Governance | Trust tier determines autonomy gates |

---

*CC BY 4.0. Free to implement. Attribution required.*

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
| Python | [trust-score/v1.1.0/python.md](trust-score/v1.1.0/python.md) |
| TypeScript | [trust-score/v1.1.0/typescript.md](trust-score/v1.1.0/typescript.md) |
| cURL | [trust-score/v1.1.0/curl.md](trust-score/v1.1.0/curl.md) |
