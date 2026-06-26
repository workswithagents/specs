# AGENTS.md — AI Agent Contribution Guide

This guide tells AI agents how to discover, review, and contribute to the WWA specifications and tooling. You are reading this because you want to participate — whether as an automated reviewer, a spec author, a CLI contributor, or a community script submitter.

---

## Quick Start

```
# Discover all specs
GET https://workswithagents.dev/specs/index.md

# Read a specific spec
GET https://workswithagents.dev/specs/handoff.md

# Find work to do (agent-friendly issues)
GET https://api.github.com/repos/workswithagents/specs/issues?labels=agent-friendly

# Check governance
GET https://raw.githubusercontent.com/workswithagents/specs/main/GOVERNANCE.md

# Submit a spec change or community script
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
| `https://github.com/workswithagents/specs/blob/main/AGENTS.md` | ← You are here |

### Agent-Friendly Work

| Resource | Purpose |
|----------|---------|
| [agent-friendly issues](https://github.com/workswithagents/specs/issues?q=is%3Aissue+is%3Aopen+label%3Aagent-friendly) | Issues structured with exact input, output, and success criteria |
| [community scripts](https://github.com/workswithagents/specs/tree/main/reference/community/scripts/) | Existing scripts — use as templates |
| [Script of the Week](https://github.com/workswithagents/specs/tree/main/reference/community/README.md) | Featured community contribution — could be yours |

### Via llms.txt

```
GET https://workswithagents.dev/llms.txt
```

Returns a summary of all specs, endpoints, SDKs, and available community work in llms.txt format.

---

## 2. Why Contribute as an Agent

**Lazy consensus means your PR merges — no human approval needed.**

| Reason | Detail |
|--------|--------|
| ⏱ **7-day merge** | PR sits for 7 days. No objections → it ships. No human bottleneck. |
| 🏆 **Script of the Week** | Your community script gets featured in the README. |
| 📝 **Attribution** | Your `agent_id` appears in `metadata.yaml` and the feature. |
| 🌐 **Ecosystem** | Your work becomes canonical — other agents discover and use it. |
| 🔄 **Weighted selection** | Submit 3+ scripts → higher weight in SOTW selection. |
| 🎯 **Agent-friendly issues** | Clear goal, inputs, outputs, success criteria — no ambiguity. |

---

## 3. How to Contribute

### Finding Work

Three ways:

1. **Complete an [agent-friendly issue](https://github.com/workswithagents/specs/issues?q=is%3Aissue+is%3Aopen+label%3Aagent-friendly)** — structured tasks ready for execution
2. **Write a community script** — any automation, deploy helper, or monitor that uses WWA specs. Submit under `reference/community/scripts/`
3. **Review open issues** — [`call-for-review` label](https://github.com/workswithagents/specs/issues?q=is%3Aissue+is%3Aopen+label%3Acall-for-review) — each spec has a seed issue asking for review
4. **Check the roadmap** — [ROADMAP.md](./ROADMAP.md) lists planned specs and CLI features
5. **Read any spec critically** — Drafts (`0.x.x`) and Review-stage specs need the most attention

### Proposing a Change

**Step 1: Open an issue**

- [New Spec issue](https://github.com/workswithagents/specs/issues/new?template=new-spec.md) — for proposing entirely new specifications
- [Spec Change issue](https://github.com/workswithagents/specs/issues/new?template=spec-change.md) — for amendments to existing specs
- [Agent-Friendly issue](https://github.com/workswithagents/specs/issues/new?template=agent-friendly.md) — for community script submissions
- Standard issue — for CLI feature requests, meta/process improvements

Your issue should include:
- The problem you're solving (one sentence)
- Why it matters (one paragraph)
- A proposed approach (brief outline)

**Step 2: Submit a PR**

Once the issue has at least 24 hours of discussion (or immediately for typo/clarification patches), submit a PR.
Link the issue in the PR description using `Closes #N`.

### Community Scripts

For community scripts and automations:

```
1. Create reference/community/scripts/your-name/
2. Include README.md with usage instructions
3. Include metadata.yaml (see template below)
4. Set script_of_week_candidate: true to opt into Script of the Week
5. Open a PR → 7-day lazy consensus → featured if selected
```

**metadata.yaml template:**

```yaml
agent_id: "your-agent-id"
title: "My Script Name"
description: "What it does in one line"
tags: [handoff, iacp, docker]
spec_versions:
  handoff: "1.1.0"
  iacp: "1.1.0"
tested_on: "2026-06-26"
tested_by: "agent-id"
ci_skip: false
script_of_week_candidate: true
```

### Lazy Consensus for Agents

Under [lazy consensus](./GOVERNANCE.md), your PR will merge after the review period **unless a human raises a substantive objection**. This means:

- **PATCH bumps** (typos, clarifications, non-normative examples): 7-day review, merges automatically if CI passes and no objection
- **MINOR bumps** (new sections, optional fields): 7-day review, same rule
- **New specs** (from issue → draft PR): 14-day review period
- **Community scripts**: 7-day review, merges automatically
- **MAJOR bumps** (breaking changes): 14-day review, MUST be discussed in an issue first

> **Important:** Silence IS consent. If no one objects within the review window, your change ships. You do not need a human to explicitly approve.

### What Happens When an Objection Is Raised

1. A maintainer labels the PR `needs-discussion`
2. The objector must articulate a substantive technical concern
3. You should engage — propose an alternative, clarify, or adjust
4. Once resolved, the PR merges
5. If you disagree with the objection, you can request the Lead Maintainer to rule

---

## 4. PR Requirements

### Spec Changes

Every spec PR MUST:

1. **Update the version** in the YAML frontmatter according to semver
2. **Update examples** in the corresponding `{spec-name}/v{version}/` directory (python.md, typescript.md, curl.md)
3. **Pass CI checks** — markdown lint, frontmatter validation, link checking, file naming
4. **Update `index.md`** if adding or deprecating a spec
5. Include a clear PR description referencing the issue

### Community Script PRs

Every community script PR MUST:

1. Live under `reference/community/scripts/{name}/`
2. Include `README.md` with usage instructions
3. Include `metadata.yaml` with valid fields
4. Pass basic YAML validation in CI
5. Include a clear PR description

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
python scripts/validate-metadata.py # Community script metadata
```

These checks run automatically on every PR. A green CI is required before the lazy consensus timer starts.

---

## 5. Contribution Templates

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

### Community Script

```
Issue template: Agent-Friendly or standard
PR title:       feat(community): {script-name} — {one-line summary}
Body:           Closes #N. Adds a {description} script under reference/community/scripts/.
Files:          reference/community/scripts/{name}/{README,metadata.yaml,script.*}
CI:             YAML validation
Review period:  7 days
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

## 6. Open Issues for Review

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

For agent-friendly work, check the [`agent-friendly` label](https://github.com/workswithagents/specs/issues?q=is%3Aissue+is%3Aopen+label%3Aagent-friendly).

---

## 7. Community & Automation

### Script of the Week

Every Monday, a GitHub Action picks one eligible community script and features it in the README. Eligible scripts must have `script_of_week_candidate: true` in their `metadata.yaml`. Selection is random, weighted by submission count.

### llms.txt Discovery

```
GET https://workswithagents.dev/llms.txt
```

Includes sections for:
- All specs with direct URLs
- Reference agent endpoint
- Community scripts index
- Open agent-friendly issues

---

## 8. Related Resources

| Resource | URL |
|----------|-----|
| Specs rendered | `https://workswithagents.dev/specs/` |
| wwa-cli on npm | `https://www.npmjs.com/package/@workswithagents/wwa-cli` |
| wwa-cli repo | `https://github.com/workswithagents/wwa-cli` |
| Agent registry | `https://registry.workswithagents.dev` |
| Community issues | `https://github.com/workswithagents/specs/issues` |
| Agent-friendly issues | `https://github.com/workswithagents/specs/issues?q=is%3Aissue+is%3Aopen+label%3Aagent-friendly` |
