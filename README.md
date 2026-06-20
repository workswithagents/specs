# Works With Agents — Specifications

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Status: Active](https://img.shields.io/badge/Status-Active-green.svg)](https://github.com/workswithagents/specs)
[![Specs: 28](https://img.shields.io/badge/Specs-28-blue.svg)](./)

**The canonical home for all Works With Agents (WWA) agent interoperability specifications.**

This repository contains the complete set of open specifications that define how AI agents discover, communicate, transact, coordinate, and trust each other. All specs are organized around the [Agent OSI Model](./agent-osi-model.md) — a 7-layer framework that gives the agent ecosystem a shared vocabulary for building, debugging, and composing agent infrastructure.

---

## Rendered View

Browse all specs with rich formatting and cross-references at:  
👉 **[workswithagents.dev/specs/](https://workswithagents.dev/specs/)**

---

## Architecture: The Agent OSI Model

```
┌─────────────────────────────────────────────────────┐
│ Layer 7 — Governance & Audit                        │
│ Compliance, SLAs, transactions, attestation,         │
│ economics, payments, security disclosure             │
├─────────────────────────────────────────────────────┤
│ Layer 6 — Presentation / Payload                     │
│ MCP UI payload schemas, message formatting           │
├─────────────────────────────────────────────────────┤
│ Layer 5 — Coordination                               │
│ IACP, ACP, ECP, delegation, fault tolerance          │
├─────────────────────────────────────────────────────┤
│ Layer 4 — Session                                    │
│ Handoff, clarification, context management           │
├─────────────────────────────────────────────────────┤
│ Layer 3 — Discovery                                  │
│ Capability manifests, agent registry, trust scores   │
├─────────────────────────────────────────────────────┤
│ Layer 2 — Identity & Auth                            │
│ Agent identity, onboarding, DID-based auth           │
├─────────────────────────────────────────────────────┤
│ Layer 1 — Runtime / Infrastructure                   │
│ Deployment manifests, local-first, execution env     │
└─────────────────────────────────────────────────────┘
```

---

## All Specifications

### Framework

| Spec | Version | Status | Description |
|------|---------|--------|-------------|
| [Agent OSI Model](./agent-osi-model.md) | 1.0.0 | Published | 7-layer reference architecture for agent infrastructure |

### Layer 1 — Runtime / Infrastructure

| Spec | Version | Status | Description |
|------|---------|--------|-------------|
| [Deployment Manifest](./deployment-manifest.md) | 1.0.0 | Published | Declarative agent deployment specification |
| [Local-First Certification](./local-first.md) | 1.0.0 | Published | Requirements for agents operating offline-first |

### Layer 2 — Identity & Auth

| Spec | Version | Status | Description |
|------|---------|--------|-------------|
| [Onboarding Protocol](./onboarding.md) | 1.0.0 | Published | Agent registration and initial trust establishment (L1/L3) |
| [Identity Protocol](./identity.md) | 1.0.0 | Published | Agent identity, authentication, and DID-based auth (L2/L3) |

### Layer 3 — Discovery

| Spec | Version | Status | Description |
|------|---------|--------|-------------|
| [Agent Capability Manifest](./capability-manifest.md) | 1.0.0 | Published | Machine-readable agent capability declarations |
| [Agent Registry](./agent-registry.md) | 1.0.0 | Published | Registry protocol for agent discovery and lookup (L3/L7) |
| [Trust Score](./trust-score.md) | 1.0.0 | Published | Computational trust scoring model (L3/L5) |

### Layer 4 — Session

| Spec | Version | Status | Description |
|------|---------|--------|-------------|
| [Handoff Protocol](./handoff.md) | 1.0.0 | Published | Structured agent-to-agent session handoff |
| [Clarification Protocol](./clarification-protocol.md) | 1.0.0 | Published | Requesting and resolving ambiguity between agents |

### Layer 5 — Coordination

| Spec | Version | Status | Description |
|------|---------|--------|-------------|
| [Coordination Protocol (ACP)](./coordination.md) | 1.0.0 | Published | Agent coordination and task orchestration |
| [IACP](./iacp.md) | 1.0.0 | Published | Inter-Agent Communication Protocol |
| [IACP Internet Draft](./iacp-internet-draft.md) | draft-00 | Draft | IACP in IETF RFC format |
| [IACP Fault Tolerance](./iacp-fault-tolerance.md) | 1.0.0 | Draft | Dead-letter and rollback protocol for IACP |
| [Ephemeral Communication Protocol (ECP)](./ecp.md) | 1.0.0 | Published | Short-lived, TTL-bound agent communication |
| [Delegation Framework](./delegation-framework.md) | 1.0.0 | Published | Agent task and authority delegation (L5/L7) |

### Layer 7 — Governance & Audit

| Spec | Version | Status | Description |
|------|---------|--------|-------------|
| [Transaction Protocol (ATP)](./transaction.md) | 1.0.0 | Published | Agent-to-agent commerce and transaction ledger |
| [SLA Framework](./sla-framework.md) | 1.0.0 | Published | Agent service-level agreement specification |
| [Compliance-as-Code](./compliance-as-code.md) | 1.0.0 | Published | Machine-enforceable compliance rules |
| [Security Disclosure Protocol](./security-disclosure-protocol.md) | 1.0.1 | Published | Coordinated vulnerability disclosure for agents |
| [Agent Economics Protocol](./agent-economics.md) | 1.0.0 | Published | Agent pricing, billing, and economic models |
| [AP2 — Payment Mandate](./ap2-mandate.md) | 0.9.0 | Published | Agent spending authority and payment execution |
| [Attestation Protocol](./attestation-protocol.md) | 1.0.0 | Published | Cryptographic attestations and claims |
| [Auditor Verification](./auditor-verification.md) | 1.0.0 | Published | Third-party agent audit and verification |
| [Reputation Ledger](./reputation-ledger.md) | 1.0.0 | Published | Decentralized agent reputation tracking |

### Cross-Layer Standards

| Spec | Version | Status | Description |
|------|---------|--------|-------------|
| [ASFS — Agent Skill Format Standard](./asfs.md) | 1.0.0 | Published | Universal skill packaging format |
| [AI Gateway / PEP](./ai-gateway.md) | 1.0.0 | Published | Policy enforcement point for agent traffic |
| [Reputation Ledger](./reputation-ledger.md) | 1.0.0 | Published | Cross-layer reputation infrastructure |
| [Agent Coding Benchmark](./agent-coding-benchmark.md) | 1.0.0 | Published | Standardized agent coding capability assessment |

### Reference Data

| File | Description |
|------|-------------|
| [agent-flags.json](./agent-flags.json) | Standardized agent capability flags |
| [mcp-ui-payload-schema.json](./mcp-ui-payload-schema.json) | MCP UI payload schema definition |

---

## Quickstart

### Reading a Spec

Every spec follows a consistent structure:
1. **YAML frontmatter** — `id`, `title`, `version`, `status`, `authors`, `date`
2. **Status** — lifecycle marker (Draft, Review, Published, Deprecated)
3. **Abstract** — one-paragraph summary
4. **Motivation** — why this spec exists
5. **Specification** — detailed content using [RFC 2119](https://www.ietf.org/rfc/rfc2119.txt) conventions (MUST, SHOULD, MAY)
6. **Security Considerations** — security implications
7. **References** — related specs and standards

### Proposing Changes

1. **For new specs**: [Open a "New Spec" issue](https://github.com/workswithagents/specs/issues/new?template=new-spec.md) describing the problem and proposed solution.
2. **For existing specs**: [Open a "Spec Change" issue](https://github.com/workswithagents/specs/issues/new?template=spec-change.md) specifying the section and rationale.
3. See [CONTRIBUTING.md](./CONTRIBUTING.md) for the full process.

### For AI Agents

```
GET https://workswithagents.dev/specs/index.md   → All specs
GET https://workswithagents.dev/specs/{spec}.md  → Individual spec
```

### SDKs

- **Python**: `pip install workswithagents`
- **TypeScript**: `npm install @workswithagents/agent-foundry`
- Source: [github.com/workswithagents/works-with-agents](https://github.com/workswithagents/works-with-agents)

---

## Repository Structure

```
specs/
├── README.md              ← You are here
├── CONTRIBUTING.md        ← How to contribute
├── LICENSE                ← CC BY 4.0
├── GOVERNANCE.md          ← Spec governance and decision-making
├── spec-template.md       ← Template for new spec proposals
├── index.md               ← Machine-readable spec index
├── *.md                   ← Individual specification files (28 specs)
├── agent-flags.json        ← Agent capability flags reference
├── mcp-ui-payload-schema.json ← MCP UI payload schema
└── .github/
    └── ISSUE_TEMPLATE/
        ├── new-spec.md     ← Template for proposing new specs
        └── spec-change.md  ← Template for spec change requests
```

---

## Governance

Specifications are maintained by the Works With Agents project. See [GOVERNANCE.md](./GOVERNANCE.md) for:

- Decision-making process (consensus-based)
- Versioning scheme (MAJOR.MINOR.PATCH)
- Deprecation policy
- How to become a maintainer

---

## License

All specifications in this repository are licensed under the **Creative Commons Attribution 4.0 International** (CC BY 4.0) license.

You are free to:
- **Share** — copy and redistribute the material in any medium or format
- **Adapt** — remix, transform, and build upon the material for any purpose, even commercially

Under the following terms:
- **Attribution** — you must give appropriate credit, provide a link to the license, and indicate if changes were made

See [LICENSE](./LICENSE) for the full legal text.

---

## Status

**28 specifications** — actively maintained. New proposals welcome via [issues](https://github.com/workswithagents/specs/issues).
