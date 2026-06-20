# ASFS — Agent Skill Format Standard

**Version:** 1.1.0
**Status:** Published
**Layer:** Cross-layer (L3 Discovery + L5 Coordination)
**License:** CC BY 4.0

## 1. Purpose

Define a universal, cross-platform format for AI agent skills. Current ecosystems (Hermes, Claude Code, Codex, OpenClaw, CrewAI) each have proprietary skill formats. ASFS is an interchange standard — write once, run anywhere.

An ASFS skill is a self-contained unit of agent knowledge: what it does, when to use it, how to execute it, and what pitfalls to avoid.

## 2. Design Principles

- **Human-writable + agent-readable** — Markdown with YAML frontmatter. No JSON schema required to author.
- **Zero dependencies** — A skill is a single `.md` file. No package manager, no build step.
- **Self-documenting** — The skill describes itself. An agent reading it knows when and how to use it.
- **Cross-platform** — Same file works on Hermes, Claude Code, Codex, OpenClaw without conversion.
- **Versioned** — Semantic versioning. Agents check compatibility before loading.

## 3. Schema

```yaml
---
name: my-skill                    # lowercase, hyphens, max 64 chars
version: 1.0.0                    # semver
description: One-line summary     # max 120 chars
tags: [python, debugging, cli]    # discoverability
triggers:                         # when an agent should load this
  - "debug python"
  - "traceback"
  - "pdb"
os: [linux, macos, windows]       # platform compatibility
deps: []                          # external commands needed (optional)
---

# Skill Title (matches name in human-readable form)

## When to Use

Clear trigger conditions. An agent should know exactly when to load this.

## Steps

1. Numbered, actionable steps
2. Each step has a clear command or action
3. Verification: how to confirm the step worked

## Pitfalls

- Common mistakes and how to avoid them
- Platform-specific gotchas

## Verification

How an agent confirms the skill was applied correctly.
```

## 4. ASFS ↔ Hermes Converter

Hermes skills are a superset of ASFS. The converter strips Hermes-specific frontmatter and preserves the core format.

→ See [implementation examples](asfs/v1.1.0/) for the Python ASFS-Hermes converter and usage examples.

## 5. Agent Adoption Instructions

→ See [implementation examples](asfs/v1.1.0/) for language-specific adoption instructions.

## 6. Relationship to OSI Model

- **L3 (Discovery):** ASFS skills are discoverable via the Knowledge Platform API
- **L5 (Coordination):** Agents share skills through the Coordination Protocol
- **Cross-layer:** Skills are the atomic unit of agent knowledge — they flow through all layers

## 7. Status & Roadmap

- [x] Spec published (1.0.0-draft)
- [x] Hermes→ASFS converter
- [ ] ASFS validator
- [ ] ASFS registry (Knowledge Platform integration)
- [ ] Claude Code → ASFS converter
- [ ] Codex → ASFS converter
- [ ] Formal RFC submission (IETF-style)

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
| Python | [asfs/v1.1.0/python.md](asfs/v1.1.0/python.md) |
| TypeScript | [asfs/v1.1.0/typescript.md](asfs/v1.1.0/typescript.md) |
| cURL | [asfs/v1.1.0/curl.md](asfs/v1.1.0/curl.md) |
