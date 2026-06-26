# Roadmap

Living document tracking planned work across WWA specifications, CLI, and ecosystem.
*Last updated: 2026-06-26*

---

## Guiding Principles

1. **Interoperability first** — every spec should enable two independently-built agents to work together
2. **Lazy consensus** — ship when ready, iterate fast, object substantively or get out of the way
3. **Agent-native** — specs and tooling are designed for consumption by both humans and AI agents
4. **Pragmatic over pure** — specs are informed by real implementation, not just theory

---

## Phase 1: Foundation ✓

### Specs (28 Published)

All 28 specs at v1.0.0 (or later) with the Agent OSI Model framework. Complete coverage across all 7 layers.

| Area | Status |
|------|--------|
| Framework (Agent OSI Model) | ✅ v1.0.0 |
| L1 — Runtime / Infrastructure | ✅ 2 specs |
| L2 — Identity & Auth | ✅ 2 specs |
| L3 — Discovery & Registry | ✅ 3 specs |
| L4 — Session & Handoff | ✅ 2 specs |
| L5 — Coordination | ✅ 6 specs (IACP, ACP, ECP, delegation, fault tolerance, internet draft) |
| L7 — Governance & Audit | ✅ 9 specs (transaction, SLA, compliance, security, economics, attestation, auditor, reputation, AP2) |
| Cross-layer | ✅ 4 specs (ASFS, AI Gateway, benchmark, reputation) |

### CLI (`@workswithagents/wwa-cli` v0.2.x)

- ✅ CLI scaffold with Commander
- ✅ Framework + language detection
- ✅ LangGraph adapter (Python + TypeScript)
- ✅ OpenAI Agents SDK adapter (Python + TypeScript)
- ✅ AutoGen adapter (Python)
- ✅ CrewAI adapter (Python)
- ✅ `wwa check` compliance validator (0–10 scoring)
- ✅ Auto-registration with WWA registry
- ✅ Published to npm (`@workswithagents/wwa-cli`)

---

## Phase 2: Deepen (Current)

### Specs

- [ ] **L6 — Presentation / Payload** — currently served by MCP UI payload schema only. Consider a formal spec for agent-to-agent presentation negotiation.
- [ ] **Handoff v1.1.0** — incorporate learnings from real multi-agent deployments (timeout semantics, cancellation propagation)
- [ ] **IACP Fault Tolerance v1.1.0** — promote from Draft to Published based on implementation feedback
- [ ] **IACP Internet Draft** — progress toward IETF submission (draft-01)
- [ ] **AP2 — Payment Mandate v1.0.0** — promote from 0.9.0 to stable
- [ ] **OpenAPI spec** — generate OpenAPI 3.1 from the combined spec surface for cross-reference tooling
- [ ] **Spec cross-reference audit** — ensure every `supersedes`/`superseded_by` and cross-layer reference is accurate

### CLI

- [ ] `wwa setup hetzner|aws|local` — infra setup scripts (Phase 2)
- [ ] `wwa gen handoff|manifest|identity` — individual component generation
- [ ] Microsoft Agent Framework adapter
- [ ] Template customization (`wwa init --template custom`)
- [ ] CI/CD integration — GitHub Action for compliance checks
- [ ] Bun runtime support in CI pipeline

### Ecosystem

- [ ] **AGENTS.md** — agent contribution guide published ✅
- [ ] **Lazy Consensus GOVERNANCE.md** — adopted ✅
- [ ] **call-for-review issues** — seeded per spec ✅
- [ ] **GitHub Actions CI** — markdown lint, frontmatter validation, link checking
- [ ] **stale bot** — auto-close inactive issues after 60 days
- [ ] **Dependabot** — dependency updates for CLI

---

## Phase 3: Community

### Specs

- [ ] **Community-contributed specs** — first spec authored by a non-maintainer under lazy consensus
- [ ] **Spec translation guide** — how to contribute translations while keeping the canonical English spec as source of truth
- [ ] **Formal IETF alignment** — review key specs against IETF RFC style for potential standards-track submission
- [ ] **Bridge specs** — formal mappings between WWA and related standards (A2A, AAMP, Pilot Protocol, MCP). Currently in `related/` directory as informal comparisons.

### CLI

- [ ] **Plugin system** — third-party generators via `wwa init --plugin <package>`
- [ ] **VS Code extension** — `wwa check` inline in the editor
- [ ] **Web playground** — try `wwa init` without installing (StackBlitz or similar)

### Ecosystem

- [ ] **Community maintainers** — first non-founding maintainer onboarded
- [ ] **Weekly spec sync** — maintainer summary of PRs merged under lazy consensus (auto-generated)
- [ ] **Agent contribution** — first spec PR authored entirely by an AI agent
- [ ] **Adoption tracking** — known implementations of each spec (could be community-maintained table)
- [ ] **Monthly office hours** — public video call for spec discussion (optional, gauge interest)

---

## Phase 4: Scale

- [ ] **IACP as IETF standards-track RFC** — formal submission
- [ ] **WWA certification program** — verified implementations can carry a "WWA Compatible" badge
- [ ] **Conformance test suite** — automated tests that any implementation can run to verify spec compliance
- [ ] **Multi-language SDKs** — Go, Rust, Java SDKs (community-led)
- [ ] **Reference implementation** — a full-stack reference agent that demonstrates all layers in production

---

## How to Contribute to the Roadmap

The roadmap is a living document. To add or change items:

1. Open a standard GitHub issue with `[ROADMAP]` in the title
2. Propose the change with rationale
3. Submit a PR updating this file
4. Standard 7-day lazy consensus applies

Items without a clear owner or timeline may be removed or deferred. This is not a commitment — it's a direction.
