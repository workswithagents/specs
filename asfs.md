# ASFS — Agent Skill Format Standard

**Version:** 1.1.0
**Status:** Published
**Layer:** Cross-layer (L3 Discovery + L5 Coordination)
**License:** CC BY 4.0

## 1. Purpose

Define a universal, cross-platform format for AI agent skills. Current ecosystems (Hermes, Claude Code, Codex, OpenClaw, CrewAI) each have proprietary skill formats. ASFS is an interchange standard — write once, run anywhere.

An ASFS skill is a self-contained unit of agent knowledge: what it does, when to use it, how to execute it, and what pitfalls to avoid.

### Problem
Every agent ecosystem (Hermes, Claude Code, Codex, OpenClaw, CrewAI) has its own proprietary skill format. A skill written for one platform is useless on another. This locks developers into ecosystems, prevents skill sharing across teams using different tools, and makes it impossible to build a cross-platform skill marketplace.

### Solution
A universal, cross-platform format for AI agent skills — a single `.md` file with YAML frontmatter that any agent framework can read. Write once, run anywhere. No dependencies, no package manager, no build step. The format is human-writable and agent-readable, with standard sections for triggers, steps, pitfalls, and verification.

### When to use
- Building portable skills that work across multiple agent frameworks
- Distributing skills through a marketplace that serves multiple ecosystems
- Teams using different agent platforms that want to share skills
- Publishing open-source skills for community reuse

### When NOT to use
- You only use one platform and never plan to switch — use the native format
- One-off tasks that won't be reused — the overhead of packaging isn't worth it
- You need tool-level protocol integration (not skill-level) — use MCP instead
- You need structured knowledge representation (not procedural skills) — use OKF

### How it compares to similar specs
| Instead of THIS | When | Because |
|---|---|---|
| MCP (Model Context Protocol) | Integrating tools at the protocol level | MCP defines how agents call tools; ASFS defines what agents know (skills, pitfalls, procedures) |
| OKF (Open Knowledge Format) | Structured, queryable knowledge representation | OKF is for knowledge graphs and facts; ASFS is for procedural skills with steps and triggers |
| Native platform formats | You're locked into one ecosystem and happy with it | Each platform's native format may have richer features specific to that platform |

### What you lose without THIS
- Skills are locked to a single platform — can't reuse across ecosystems
- No cross-platform skill marketplace can exist
- Teams using different agent frameworks can't share institutional knowledge
- Migrating between platforms means rewriting all skills from scratch

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
