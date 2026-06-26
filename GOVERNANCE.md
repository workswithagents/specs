# Governance

This document defines how the Works With Agents (WWA) specifications and tooling are governed, how decisions are made, and how the project evolves.

---

## Project Ownership

The WWA project is maintained by the **Works With Agents project**, stewarded by [Vilius Vystartas](https://github.com/vystartasv). The project operates as an open, community-driven standards effort that includes:

- **Specifications** — `workswithagents/specs` — agent interoperability protocol specs
- **CLI** — `@workswithagents/wwa-cli` — framework adapter generator
- **SDKs** — Python + TypeScript reference implementations
- **Registry** — `registry.workswithagents.dev` — agent registration

All specifications are released under the [Creative Commons Attribution 4.0 International](./LICENSE) (CC BY 4.0) license. SDKs and CLI tooling use the MIT license. Anyone is free to use, share, and build upon them with proper attribution.

---

## Maintainers

Maintainers are individuals with commit access to this repository. They are responsible for:

- Reviewing and merging pull requests
- Managing the spec lifecycle (Draft → Review → Published → Deprecated)
- Enforcing [CONTRIBUTING.md](./CONTRIBUTING.md) standards
- Facilitating community discussion
- Resolving disputes when substantive objections are raised

### Current Maintainers

| Name | GitHub | Role |
|------|--------|------|
| Vilius Vystartas | [vystartasv](https://github.com/vystartasv) | Lead Maintainer |
| Pelin Kayhan | [pelinoloji](https://github.com/pelinoloji) | Maintainer |

### Becoming a Maintainer

Contributors who demonstrate sustained, high-quality contributions may be nominated to become maintainers. The process:

1. **Eligibility**: At least 3 substantive contributions (authored or significantly revised specs, meaningful CLI features, or ecosystem improvements)
2. **Nomination**: By an existing maintainer, via a GitHub issue
3. **Review**: 14-day review period for community feedback
4. **Decision**: No sustained objections from existing maintainers; nominee acceptance
5. **Onboarding**: New maintainer receives write access and is added to this document

---

## Decision-Making: Lazy Consensus

Spec changes are decided by **lazy consensus**, modeled on the [Apache Foundation's consensus model](https://www.apache.org/foundation/glossary.html#LazyConsensus).

### What Lazy Consensus Means

**Silence is consent.** A PR merges automatically after the review period unless a substantive objection is raised. You do not need approval — you need absence of blockers.

This applies to both human contributors and AI agents. The spec repository includes an [AGENTS.md](./AGENTS.md) with API-driven contribution instructions for automated participants.

### What It Does NOT Mean

- Unanimous agreement
- Absence of any review
- No accountability for changes

### Substantive Objections

An objection is **substantive** if it:
- Identifies a specific technical flaw in the proposal
- Demonstrates that the proposal would harm interoperability
- Shows that the proposal contradicts an existing Published spec

Non-substantive objections (e.g., personal preference, stylistic disagreements, "I don't like it") do not block consensus.

### Lazy Consensus Process

1. **Proposal**: Made via [GitHub issue](https://github.com/workswithagents/specs/issues) or pull request
2. **Review period**: 7 days for non-trivial changes, 14 days for new specs (7 days for agent-contributed changes that pass CI)
3. **Default outcome**: If no substantive objections within the review period, the PR merges
4. **Objection raised**: A maintainer facilitates resolution — the objector and proposer work toward a mutually acceptable change
5. **Resolution**: Once all substantive objections are addressed, the PR merges
6. **Escalation**: If resolution cannot be reached, the Lead Maintainer makes a final decision after considering all input

### Maintainer's Role

Maintainers do not gatekeep. Their role is to:
- Ensure the review period runs fairly
- Distinguish substantive objections from stylistic ones
- Facilitate resolution when objections arise
- Merge unblocked PRs (ideally automated via CI)

---

## Versioning

Specifications follow [Semantic Versioning](https://semver.org/) (MAJOR.MINOR.PATCH), adapted for standards documents:

### MAJOR (`X.0.0`)

A MAJOR version bump indicates **breaking changes**. Implementations that conformed to the previous MAJOR version may not conform to the new version. Examples:
- Removing a normative requirement
- Changing a `MUST` to `MUST NOT` (or vice versa)
- Altering the wire format, schema, or protocol in incompatible ways
- Adding a new mandatory requirement that existing implementations cannot satisfy

### MINOR (`0.Y.0`)

A MINOR version bump indicates **new functionality** that is backward-compatible. Examples:
- Adding new optional fields or messages
- Adding new normative sections
- Expanding guidance while keeping all existing MUST/SHOULD requirements intact

### PATCH (`0.0.Z`)

A PATCH version bump indicates **clarifications** with no normative changes. Examples:
- Fixing typos and grammar
- Adding non-normative examples
- Clarifying ambiguous language without changing requirements

### Pre-Release Versions

Draft specs use versions `0.x.x`. Pre-release tags (e.g., `1.0.0-rc1`) MAY be used for Review-stage specs.

### CLI Versioning

The `wwa-cli` follows its own semver schedule but aligns MAJOR bumps with spec MAJOR bumps that affect generated adapter code.

---

## Deprecation Policy

A specification MAY be deprecated when:

- It is fully superseded by a newer specification
- The protocol or approach it describes is no longer recommended
- It has been unmaintained and no implementations exist

### Deprecation Process

1. **Proposal**: A [Spec Change issue](https://github.com/workswithagents/specs/issues/new?template=spec-change.md) is opened proposing deprecation, with rationale
2. **Discussion**: Minimum 14-day review period
3. **Consensus**: Lazy consensus applies (see above)
4. **Implementation**:
   - The spec's `status` is changed to `Deprecated`
   - A `superseded_by` field is added to the frontmatter (if applicable)
   - The replacement spec is referenced prominently
   - A deprecation notice is added to the spec body
5. **Archive**: Deprecated specs remain in the repository permanently for historical reference. They are never deleted.

---

## Roadmap

The project maintains a [ROADMAP.md](./ROADMAP.md) that tracks planned work across specs, CLI, and ecosystem. The roadmap is a living document — updated via PR under lazy consensus.

---

## Code of Conduct

This project follows the [Contributor Covenant v2.1](https://www.contributor-covenant.org/version/2/1/code_of_conduct/). All participants are expected to uphold these standards.

---

## Changes to This Document

This governance document itself follows the same decision-making process as specifications. Changes are proposed via PR, discussed, and merged under lazy consensus.

---

## Contact

For governance questions, open a [GitHub issue](https://github.com/workswithagents/specs/issues) or contact the maintainers directly.
