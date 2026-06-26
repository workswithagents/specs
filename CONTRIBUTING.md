# Contributing to WWA Specifications

Thank you for helping build the open standards for AI agent interoperability.

This guide covers how to propose new specifications, suggest changes to existing ones, and participate in the review process. AI agents should read [AGENTS.md](./AGENTS.md) for the API-driven contribution workflow.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Ways to Contribute](#ways-to-contribute)
- [AI Agent Contributions](#ai-agent-contributions)
- [Spec Lifecycle](#spec-lifecycle)
- [Proposing a New Spec](#proposing-a-new-spec)
- [Suggesting Changes to Existing Specs](#suggesting-changes-to-existing-specs)
- [Spec File Requirements](#spec-file-requirements)
- [Style Guide](#style-guide)
- [Review Process](#review-process)
- [CI Expectations](#ci-expectations)

---

## Code of Conduct

This project follows the [Contributor Covenant v2.1](https://www.contributor-covenant.org/version/2/1/code_of_conduct/). By participating, you agree to uphold its standards. We expect all contributors to treat each other with respect and professionalism.

---

## Ways to Contribute

| Contribution Type | Process |
|------------------|---------|
| **New specification** | Open a [New Spec issue](https://github.com/workswithagents/specs/issues/new?template=new-spec.md) → Discuss → Draft PR → 14-day lazy consensus → Merge |
| **Specification change** | Open a [Spec Change issue](https://github.com/workswithagents/specs/issues/new?template=spec-change.md) → Discuss → PR → 7-day lazy consensus → Merge |
| **Clarification / typo fix** | Open a PR directly with explanation → 7-day lazy consensus → Merge |
| **Meta / process improvement** | Open a standard GitHub issue → PR → 7-day lazy consensus → Merge |
| **AI agent contribution** | See [AGENTS.md](./AGENTS.md) for API-driven workflow |

> **Lazy consensus** means your PR merges after the review period unless someone raises a substantive technical objection. Silence is consent.

---

## AI Agent Contributions

AI agents are first-class participants in this project. See [AGENTS.md](./AGENTS.md) for a dedicated guide covering:

- 🔍 **Discovery** — how to find specs via API, llms.txt, or GitHub
- 📝 **Contribution workflow** — issue → PR → lazy consensus → merge
- ⏱ **Shorter review periods** — agent-contributed PRs that pass CI get a 7-day timer (vs 14 days for human new specs)
- 📋 **PR templates** — structured prompts for PATCH, MINOR, new spec, and CLI changes
- 🧪 **CI requirements** — what must pass before the timer starts

---

## Spec Lifecycle

Every specification moves through four stages:

```
Draft → Review → Published → Deprecated
```

### Draft

A spec begins as **Draft** when a PR is first merged. Draft specs are works-in-progress:
- They may change substantially
- Implementations SHOULD NOT rely on Draft specs in production
- Drafts are identified by version `0.x.x`

### Review

A spec enters **Review** when the authors believe it is stable and ready for wider scrutiny:
- A review period of at least 14 days is opened
- All substantive concerns must be addressed before publication
- The spec may return to Draft if major issues are discovered

### Published

A **Published** spec is considered stable and suitable for implementation:
- Published specs carry version `1.x.x` or higher
- Breaking changes to Published specs require a MAJOR version bump
- Implementations MAY rely on Published specs in production

### Deprecated

A spec enters **Deprecated** status when it is superseded or no longer recommended:
- Deprecated specs remain in the repository for historical reference
- The deprecation notice MUST reference the replacement spec (if any)
- Deprecated specs are not actively maintained

---

## Proposing a New Spec

1. **Check for duplicates.** Search [existing issues](https://github.com/workswithagents/specs/issues) and the [spec index](./index.md) to ensure your idea hasn't already been addressed.

2. **Open a [New Spec issue](https://github.com/workswithagents/specs/issues/new?template=new-spec.md).** Include:
   - A clear spec name
   - The relevant Agent OSI Model layer(s)
   - A concise problem statement
   - A proposed solution outline

3. **Discussion.** The community and maintainers will discuss scope, overlap with existing specs, and feasibility. This may take days to weeks.

4. **Draft the spec.** Once there is consensus to proceed, draft the spec using [spec-template.md](./spec-template.md):
   - Use the YAML frontmatter format
   - Follow the [style guide](#style-guide)
   - Set version to `0.1.0` and status to `Draft`
   - Place the file in the repository root with a descriptive kebab-case filename (e.g., `my-new-protocol.md`)

5. **Submit a PR.** Open a pull request with your draft spec. Link the issue in the PR description.

6. **Review and merge.** The PR will be reviewed. Once approved and any requested changes are made, it will be merged.

---

## Suggesting Changes to Existing Specs

1. **Open a [Spec Change issue](https://github.com/workswithagents/specs/issues/new?template=spec-change.md).** Include:
   - The spec name and version
   - The specific section or line reference
   - The proposed change (add, modify, remove)
   - The rationale for the change

2. **Discussion.** The community evaluates the impact:
   - **Patch changes** (clarifications, typo fixes) → fast-track
   - **Minor changes** (new sections, expanded guidance) → standard review
   - **Major changes** (breaking changes, removed features) → extended review, MAJOR version bump required

3. **Submit a PR** with the changes. Update the version according to [semantic versioning](#versioning).

---

## Spec File Requirements

Every specification file MUST include the following YAML frontmatter at the top:

```yaml
---
id: your-spec-id
title: Your Spec Name
version: 0.1.0
status: Draft
authors: [Your Name]
date: YYYY-MM-DD
---
```

### Required Frontmatter Fields

| Field | Description | Example |
|-------|-------------|---------|
| `id` | Unique kebab-case identifier | `agent-osi-model` |
| `title` | Human-readable spec name | `Agent OSI Model` |
| `version` | Semantic version (MAJOR.MINOR.PATCH) | `1.0.0` |
| `status` | One of: `Draft`, `Review`, `Published`, `Deprecated` | `Published` |
| `authors` | List of author names | `[Vilius Vystartas]` |
| `date` | ISO 8601 date (YYYY-MM-DD) | `2026-05-13` |

### Optional Frontmatter Fields

| Field | Description |
|-------|-------------|
| `layer` | Agent OSI Model layer(s) — e.g., `L5`, `L3/L5` |
| `supersedes` | Reference to a spec or section this replaces |
| `superseded_by` | Reference to the spec that replaces this one |
| `license` | Always `CC BY 4.0` (can be omitted; repo LICENSE applies) |

---

## Style Guide

### RFC 2119 Keywords

All normative spec language MUST use the standard [RFC 2119](https://www.ietf.org/rfc/rfc2119.txt) keywords:

| Keyword | Meaning |
|---------|---------|
| **MUST** / **MUST NOT** | Absolute requirement or prohibition |
| **SHOULD** / **SHOULD NOT** | Strong recommendation; valid reasons may exist to ignore |
| **MAY** | Truly optional |

These keywords MUST be capitalized when used with their RFC 2119 meaning, to distinguish them from ordinary English usage.

### IETF-Style Language

- Write in clear, precise, technical English
- Define terms before using them
- Use consistent terminology throughout
- Avoid ambiguous pronouns — prefer "the agent" over "it"
- Include concrete examples for non-trivial requirements
- Number sections for easy reference (e.g., `## 3.1. Discovery Handshake`)

### Spec Structure

Every spec SHOULD include these sections, in this order:

1. **YAML frontmatter** (required)
2. **Title** — `#` heading matching `title` in frontmatter
3. **Status** — brief lifecycle note
4. **Abstract** — one-paragraph summary
5. **Motivation** — why this spec exists
6. **Specification** — the detailed normative content
7. **Security Considerations** — security implications and mitigations
8. **References** — related specs, RFCs, and standards

### Layer Table in the Index

When adding a new spec, update [index.md](./index.md) to add a row following this format:

```markdown
| Layer | [Spec Name](spec-file.md) | x.y.z | Status |
```

The layer column should use one of: `Framework`, `L1`, `L2`, `L3`, `L4`, `L5`, `L6`, `L7`, `Cross-layer`, or combinations like `L3/L5`.

---

## Review Process

### Decision-Making

Spec changes are decided by **lazy consensus**, not majority vote. The process is:

1. A proposal is made via issue or PR
2. Review period: 7 days for non-trivial changes, 14 days for new specs (7 days for agent-contributed changes that pass CI)
3. If no substantive objections → the PR merges at the end of the review period
4. Objections MUST be substantive and relate to the spec's technical merit
5. If an objection is raised, maintainers facilitate resolution
6. Once all substantive objections are addressed, the PR merges
7. The Lead Maintainer has final say on deadlocked objections

### Maintainer Responsibilities

Maintainers are responsible for:
- Facilitating constructive discussion
- Ensuring proposals follow the spec lifecycle
- Verifying frontmatter and formatting requirements
- Merging approved PRs
- Managing version bumps correctly

### Becoming a Maintainer

Contributors who demonstrate sustained, high-quality contributions may be nominated as maintainers. Nomination requires:
- At least 3 substantive contributions (specs authored or significantly revised)
- Nomination by an existing maintainer
- No sustained objections from other maintainers
- Acceptance by the nominee

---

## CI Expectations

All PRs are validated by automated checks:

- **Markdown lint** — All `.md` files must pass markdownlint
- **Frontmatter validation** — YAML frontmatter must include all required fields
- **Link checking** — Internal links must resolve
- **File naming** — Spec files must use kebab-case

Run checks locally before submitting:

```bash
# Markdown lint
npm install -g markdownlint-cli
markdownlint '**/*.md'

# Frontmatter check (Python)
pip install pyyaml
python scripts/validate-frontmatter.py
```

---

## Versioning

Spec versions follow [Semantic Versioning](https://semver.org/) (MAJOR.MINOR.PATCH):

| Bump | When |
|------|------|
| **MAJOR** (`2.0.0`) | Breaking changes — implementations must update to remain compliant |
| **MINOR** (`1.1.0`) | New sections, expanded guidance, new normative requirements (backward-compatible) |
| **PATCH** (`1.0.1`) | Clarifications, typo fixes, non-normative improvements |

## Versioned Examples

Every new spec version **MUST** include implementation examples. Examples validate that the spec is implementable and provide copy-paste reference code for agents and developers.

### Example Directory Structure

For each spec file `{spec-name}.md` with version `{version}`:

```
{spec-name}/
  v{version}/
    python.md    — Complete, runnable Python implementation
    typescript.md — Complete, runnable TypeScript implementation
    curl.md       — cURL command examples for each API endpoint
```

### Requirements

1. **Every new version** (MAJOR, MINOR, or PATCH bump) must include or update examples in the corresponding version directory
2. **Examples must be runnable** — copy-paste should work
3. **Examples must match the spec** — use real field names, real error handling, real message shapes
4. **The spec file must link** to examples via an `## Examples` section (see spec-template.md for format)
5. **PRs without examples for the version are incomplete** and will not be merged

### Updating Examples

- **PATCH bump** (typo fix): Update existing examples in the same version directory
- **MINOR bump** (new features): Create new version directory with updated examples
- **MAJOR bump** (breaking changes): Create new version directory; old version directory is preserved for reference

---

## Questions?

Open a [GitHub issue](https://github.com/workswithagents/specs/issues) or reach out to the maintainers.
