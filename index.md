# Works With Agents — Specifications

Agent infrastructure specifications. Each spec addresses a specific layer of the Agent OSI Model.

## Published Specs

| Layer | Spec | Version | Status |
|-------|------|---------|--------|
| Framework | [Agent OSI Model](agent-osi-model.md) | 1.0.0 | Published |
| Cross-framework | [ASFS — Agent Skill Format Standard](asfs.md) | 1.0.0 | Published |
| L1/L3 | [Onboarding Protocol](onboarding.md) | 1.0.0 | Published |
| L2/L3 | [Identity Protocol](identity.md) | 1.0.0 | Published |
| L3 — Discovery | [Agent Capability Manifest](capability-manifest.md) | 1.0.0 | Published |
| L3 / L7 | [Agent Registry](agent-registry.md) | 1.0.0 | Published |
| Cross-layer | [AI Gateway / PEP](ai-gateway.md) | 1.0.0 | Published |
| L5 / L7 | [Delegation Framework](delegation-framework.md) | 1.0.0 | Published |
| L3/L5 | [Trust Score](trust-score.md) | 1.0.0 | Published |
| L4 — Session | [Handoff Protocol](handoff.md) | 1.0.0 | Published |
| L4 — Session | [Clarification Protocol](clarification-protocol.md) | 1.0.0 | Published |
| L5 — Coordination | [Coordination Protocol (ACP)](coordination.md) | 1.0.0 | Published |
| L5 — Coordination | [IACP — Inter-Agent Communication](iacp.md) | 1.0.0 | Published |
| Cross-layer | [Deployment Manifest](deployment-manifest.md) | 1.0.0 | Published |
| Cross-layer | [Local-First Certification](local-first.md) | 1.0.0 | Published |
| L7 — Governance | [Transaction Protocol (ATP)](transaction.md) | 1.0.0 | Published |
| L7 — Governance | [SLA Framework](sla-framework.md) | 1.0.0 | Published |
| L7 — Governance | [Compliance-as-Code](compliance-as-code.md) | 1.0.0 | Published |
| L7 — Governance | [Security Disclosure Protocol](security-disclosure-protocol.md) | 1.0.1 | Published |
| L7 — Governance | [Agent Economics Protocol](agent-economics.md) | 1.0.0 | Published |
| L7 — Audit | [Attestation Protocol](attestation-protocol.md) | 1.0.0 | Published |
| L7 — Audit | [Auditor Verification](auditor-verification.md) | 1.0.0 | Published |
| Cross-layer | [Reputation Ledger](reputation-ledger.md) | 1.0.0 | Published |
| Cross-layer | [Agent Coding Benchmark](agent-coding-benchmark.md) | 1.0.0 | Published |
| L5 — Coordination | [Ephemeral Communication Protocol (ECP)](ecp.md) | 1.0.0 | Published |
| L5 | [IACP Internet Draft](iacp-internet-draft.md) | draft-00 | Draft |

## SDK

Python reference implementations: `pip install workswithagents`
TypeScript SDK: `npm install @workswithagents/agent-foundry`

| Module | Protocol |
|--------|----------|
| `trust_score.py` | Trust Score |
| `deployment.py` | Deployment Manifest |
| `sla.py` | SLA Framework |
| `identity.py` | Identity Protocol |
| `compliance.py` | Compliance-as-Code |
| `onboarding.py` | Onboarding Protocol |
| `asfs_convert.py` | ASFS — Skill Format Converter |

Source: [github.com/workswithagents/works-with-agents](https://github.com/workswithagents/works-with-agents)

## Quick Reference

### For AI Agents
```
GET https://workswithagents.dev/specs/index.md                  → All specs
GET https://workswithagents.dev/specs/agent-osi-model.md        → Framework
GET https://workswithagents.dev/specs/asfs.md                   → Skill Format Standard
GET https://workswithagents.dev/specs/trust-score.md            → Trust Score
GET https://workswithagents.dev/specs/deployment-manifest.md    → Deployment
GET https://workswithagents.dev/specs/sla-framework.md          → SLA
GET https://workswithagents.dev/specs/identity.md               → Identity
GET https://workswithagents.dev/specs/compliance-as-code.md     → Compliance
GET https://workswithagents.dev/specs/onboarding.md             → Onboarding
GET https://workswithagents.dev/specs/capability-manifest.md    → Capabilities
GET https://workswithagents.dev/specs/agent-registry.md         → Agent Registry
GET https://workswithagents.dev/specs/ai-gateway.md             → AI Gateway / PEP
GET https://workswithagents.dev/specs/delegation-framework.md   → Delegation Framework
GET https://workswithagents.dev/specs/handoff.md                → Handoff
GET https://workswithagents.dev/specs/clarification-protocol.md → Clarification
GET https://workswithagents.dev/specs/coordination.md           → Coordination
GET https://workswithagents.dev/specs/iacp.md                   → IACP
GET https://workswithagents.dev/specs/iacp-internet-draft.md    → IACP (RFC format)
GET https://workswithagents.dev/specs/transaction.md            → Transactions
GET https://workswithagents.dev/specs/agent-economics.md        → Economics
GET https://workswithagents.dev/specs/attestation-protocol.md   → Attestation
GET https://workswithagents.dev/specs/auditor-verification.md   → Auditor Verification
GET https://workswithagents.dev/specs/reputation-ledger.md      → Reputation
GET https://workswithagents.dev/specs/local-first.md            → Local-First
GET https://workswithagents.dev/specs/agent-coding-benchmark.md → Coding Benchmark
GET https://workswithagents.dev/specs/security-disclosure-protocol.md → Security Disclosure
```

### For Humans
All specs: https://workswithagents.dev/specs/
Python SDK: `pip install workswithagents`
TypeScript SDK: `npm install @workswithagents/agent-foundry`

## License

All specifications: CC BY 4.0 — Free to use, cite, and build upon. Attribution required.
All reference implementations: CC BY 4.0.
