# Governance

This document defines how the Works With Agents (WWA) specifications are governed, how decisions are made, and how the project evolves.

---

## Project Ownership

The WWA specifications are maintained by the **Works With Agents project**, stewarded by [Vilius Vystartas](https://github.com/vystartasv). The project operates as an open, community-driven standards effort.

All specifications are released under the [Creative Commons Attribution 4.0 International](./LICENSE) (CC BY 4.0) license. Anyone is free to use, share, and build upon them with proper attribution.

---

## Maintainers

Maintainers are individuals with commit access to this repository. They are responsible for:

- Reviewing and merging pull requests
- Managing the spec lifecycle (Draft → Review → Published → Deprecated)
- Enforcing [CONTRIBUTING.md](./CONTRIBUTING.md) standards
- Facilitating community discussion
- Declaring consensus on proposals

### Current Maintainers

| Name | GitHub | Role |
|------|--------|------|
| Vilius Vystartas | [vystartasv](https://github.com/vystartasv) | Lead Maintainer |

### Becoming a Maintainer

Contributors who demonstrate sustained, high-quality contributions may be nominated to become maintainers. The process:

1. **Eligibility**: At least 3 substantive contributions (authored or significantly revised specs)
2. **Nomination**: By an existing maintainer, via a GitHub issue
3. **Review**: 14-day review period for community feedback
4. **Decision**: No sustained objections from existing maintainers; nominee acceptance
5. **Onboarding**: New maintainer receives write access and is added to this document

---

## Decision-Making Process

Spec changes are decided by **rough consensus**, modeled on the [IETF consensus process](https://www.ietf.org/about/participate/tao/).

### Rough Consensus

Rough consensus means that all **substantive, technical objections** have been addressed. It does NOT mean:
- Unanimous agreement
- Majority vote
- Absence of any objection

An objection is **substantive** if it:
- Identifies a specific technical flaw in the proposal
- Demonstrates that the proposal would harm interoperability
- Shows that the proposal contradicts an existing Published spec

Non-substantive objections (e.g., personal preference, stylistic disagreements) do not block consensus.

### Consensus Process

1. **Proposal**: Made via [GitHub issue](https://github.com/workswithagents/specs/issues) using the appropriate template
2. **Discussion**: Minimum 7 days for non-trivial changes, 14 days for new specs
3. **Assessment**: A maintainer evaluates whether rough consensus exists
4. **Declaration**: The maintainer declares consensus (or lack thereof) and summarizes the rationale
5. **Appeal**: If consensus is disputed, any participant may request the maintainer reconsider. The maintainer's second ruling is final unless overridden by another maintainer.

### Tie-Breaking

If the maintainers cannot reach agreement among themselves, the Lead Maintainer makes the final decision after considering all input.

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

---

## Deprecation Policy

A specification MAY be deprecated when:

- It is fully superseded by a newer specification
- The protocol or approach it describes is no longer recommended
- It has been unmaintained and no implementations exist

### Deprecation Process

1. **Proposal**: A [Spec Change issue](https://github.com/workswithagents/specs/issues/new?template=spec-change.md) is opened proposing deprecation, with rationale
2. **Discussion**: Minimum 14-day review period
3. **Consensus**: Rough consensus is required (see above)
4. **Implementation**:
   - The spec's `status` is changed to `Deprecated`
   - A `superseded_by` field is added to the frontmatter (if applicable)
   - The replacement spec is referenced prominently
   - A deprecation notice is added to the spec body
5. **Archive**: Deprecated specs remain in the repository permanently for historical reference. They are never deleted.

---

## Code of Conduct

This project follows the [Contributor Covenant v2.1](https://www.contributor-covenant.org/version/2/1/code_of_conduct/). All participants are expected to uphold these standards.

---

## Changes to This Document

This governance document itself follows the same decision-making process as specifications. Changes are proposed via PR, discussed, and merged upon rough consensus.

---

## Contact

For governance questions, open a [GitHub issue](https://github.com/workswithagents/specs/issues) or contact the maintainers directly.
