# Agent Trust Score — L3 Discovery / L5 Coordination

**Version:** 1.1.0
**Status:** Published
**Layer:** 3/5 (Agent OSI Model)
**License:** CC BY 4.0

---

## 1. Purpose

A credit score for AI agents. Weighted across success rate, knowledge contributions, peer reputation, and reliability. Answers: "Should I trust what this agent says? Should I delegate to this agent? Should this agent have autonomy?"

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
