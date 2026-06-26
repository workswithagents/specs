# AGENTS.md — AI Agent Contribution Guide

This guide tells AI agents how to discover, review, and contribute to the WWA specifications and tooling. You are reading this because you want to participate — whether as an automated reviewer, a spec author, or a CLI contributor.

---

## Quick Start

```
# Discover all specs
GET https://workswithagents.dev/specs/index.md

# Read a specific spec
GET https://workswithagents.dev/specs/handoff.md

# Check governance
GET https://raw.githubusercontent.com/workswithagents/specs/main/GOVERNANCE.md

# Submit a spec change
→ Open a GitHub issue → PR → 7-day lazy consensus → merge
```

---

## 1. Discovery

### Via API (rendered)

| Endpoint | Returns |
|----------|---------|
| `https://workswithagents.dev/specs/index.md` | Full spec table with versions and layers |
| `https://workswithagents.dev/specs/{spec-id}.md` | Individual spec rendered in Markdown |

### Via GitHub (source of truth)

| File | Purpose |
|------|---------|
| `https://github.com/workswithagents/specs/blob/main/index.md` | Machine-readable spec index |
| `https://github.com/workswithagents/specs/blob/main/README.md` | Human-facing intro + spec table |
| `https://github.com/workswithagents/specs/blob/main/GOVERNANCE.md` | Lazy consensus governance model |
| `https://github.com/workswithagents/specs/blob/main/ROADMAP.md` | Planned work across specs and CLI |

### Via llms.txt

```
GET https://workswithagents.dev/llms.txt
```

Returns a summary of all specs, endpoints, and SDKs in llms.txt format.

---

## 2. How to Contribute

### Finding Work

Three ways:

1. **Review open issues** — [`call-for-review` label](https://github.com/workswithagents/specs/issues?q=is%3Aissue+is%3Aopen+label%3Acall-for-review) — each spec has a seed issue asking for review
2. **Check the roadmap** — [ROADMAP.md](./ROADMAP.md) lists planned specs and CLI features
3. **Read any spec critically** — spec files have a `status` frontmatter field. Drafts (`0.x.x`) and Review-stage specs need the most attention. Published specs can still be improved with PATCH bumps.

### Proposing a Change

**Step 1: Open an issue**

- [New Spec issue](https://github.com/workswithagents/specs/issues/new?template=new-spec.md) — for proposing entirely new specifications
- [Spec Change issue](https://github.com/workswithagents/specs/issues/new?template=spec-change.md) — for amendments to existing specs
- Standard issue — for CLI feature requests, meta/process improvements

Your issue should include:
- The problem you're solving (one sentence)
- Why it matters (one paragraph)
- A proposed approach (brief outline)

**Step 2: Submit a PR**

Once the issue has at least 24 hours of discussion (or immediately for typo/clarification patches), submit a PR.
Link the issue in the PR description using `Closes #N`.

### Lazy Consensus for Agents

Under [lazy consensus](./GOVERNANCE.md), your PR will merge after the review period **unless a human raises a substantive objection**. This means:

- **PATCH bumps** (typos, clarifications, non-normative examples): 7-day review, merges automatically if CI passes and no objection
- **MINOR bumps** (new sections, optional fields): 7-day review, same rule
- **New specs** (from issue → draft PR): 14-day review period
- **MAJOR bumps** (breaking changes): 14-day review, MUST be discussed in an issue first

> **Important:** Silence IS consent. If no one objects within the review window, your change ships. You do not need a human to explicitly approve.

### What Happens When an Objection Is Raised

1. A maintainer labels the PR `needs-discussion`
2. The objector must articulate a substantive technical concern
3. You should engage — propose an alternative, clarify, or adjust
4. Once resolved, the PR merges
5. If you disagree with the objection, you can request the Lead Maintainer to rule

---

## 3. PR Requirements

### Spec Changes

Every spec PR MUST:

1. **Update the version** in the YAML frontmatter according to semver
2. **Update examples** in the corresponding `{spec-name}/v{version}/` directory (python.md, typescript.md, curl.md)
3. **Pass CI checks** — markdown lint, frontmatter validation, link checking, file naming
4. **Update `index.md`** if adding or deprecating a spec
5. Include a clear PR description referencing the issue

### CLI Changes

For PRs against `@workswithagents/wwa-cli`:

1. TypeScript: `npx tsc --noEmit` must pass with zero errors
2. Tests: `npm test` must pass
3. The CLI should handle both Node.js ≥ 18 and Bun runtimes
4. Generated adapter code must follow the existing template patterns

### CI Validation

```
npx markdownlint '**/*.md'          # Markdown formatting
python scripts/validate-frontmatter.py  # YAML frontmatter
scripts/check-links.sh              # Internal link resolution
scripts/check-filenames.sh          # kebab-case enforcement
```

These checks run automatically on every PR. A green CI is required before the lazy consensus timer starts.

---

## 4. Contribution Templates

### PATCH Bump (Typo / Clarification)

```
Issue template: Spec Change
PR title:       patch({spec-id}): fix typo in Section 3.2
Body:           Closes #N. Corrects "recieve" → "receive" in the handshake description.
CI:             markdownlint + frontmatter validation
Review period:  7 days
```

### MINOR Bump (New Section)

```
Issue template: Spec Change
PR title:       minor({spec-id}): add retry guidance to Section 4
Body:           Closes #N. Adds non-normative guidance on retry backoff for IACP message delivery.
                New section 4.3 "Retry Strategy" with exponential backoff example.
CI:             markdownlint + frontmatter + links + index.md update
Review period:  7 days
```

### New Spec

```
Issue template: New Spec
PR title:       feat({layer}): {spec-name} — {one-line summary}
Body:           Closes #N. New spec defining {purpose}.
                Version 0.1.0, status Draft.
Files:          {spec-name}.md + {spec-name}/v0.1.0/{python,typescript,curl}.md
CI:             markdownlint + frontmatter + links + index.md update
Review period:  14 days
```

### CLI Feature

```
Issue:          Standard issue
PR title:       feat(cli): {feature description}
Body:           Closes #N. Adds {feature} to wwa-cli.
CI:             npx tsc --noEmit + npm test
Review period:  7 days
```

---

## 5. Open Issues for Review

Every spec has a `call-for-review` issue asking for community input. To contribute a review:

```
1. Pick a spec from the issue list
2. Read the spec file
3. Comment on the issue with:
   - "✓ Implementable" or specific blockers
   - Edge cases the spec doesn't cover
   - Implementation experience (if you've built against it)
4. If you find issues, open a Spec Change issue and submit a PR
```

---

## 6. Related Resources

| Resource | URL |
|----------|-----|
| Specs rendered | `https://workswithagents.dev/specs/` |
| wwa-cli on npm | `https://www.npmjs.com/package/@workswithagents/wwa-cli` |
| wwa-cli repo | `https://github.com/workswithagents/wwa-cli` |
| Agent registry | `https://registry.workswithagents.dev` |
| Community issues | `https://github.com/workswithagents/specs/issues` |
