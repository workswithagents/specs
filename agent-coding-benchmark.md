---
id: agent-coding-benchmark
title: Agent Coding Benchmark
version: 1.0.0
status: Published
authors: [Vilius Vystartas]
date: 2026-05-13
---

# Agent Coding Benchmark Methodology

## Overview

We test LLMs on 10 real-world agent coding tasks — the things agents
actually do: parse files, query SQLite, fix bugs, extract with regex,
validate JSON schemas, fetch concurrently, monitor processes, and
recover from errors.

### Problem
Evaluating LLMs for real agent use cases is hard. Existing benchmarks test academic NLP tasks (GLUE, MMLU) or ML training throughput (MLPerf), not the actual tool-use, error-recovery, and practical reasoning agents need. Without a standard benchmark, teams pick models on vibes or vendor claims, and there's no way to compare providers on the same real-world agent tasks.

### Solution
A 10-task benchmark that tests exactly what agents do: parse files, query SQLite, fix bugs, extract with regex, validate JSON schemas, fetch concurrently, monitor processes, and recover from errors. Every model runs the same tasks under the same tight token budget (40K per task), producing comparable scores that reflect practical agent capability and efficiency.

### When to use
- Comparing LLM providers for agent workloads before committing to one
- Publishing benchmark scores to establish model credibility
- Selecting a model for a specific coding agent deployment
- Testing whether a new model version is actually better at agent tasks

### When NOT to use
- You need NLP benchmarks like MMLU, GLUE, or HellaSwag — use HELM instead
- You're benchmarking ML training/inference throughput — use MLPerf
- You're evaluating general-purpose agent reasoning (not coding) — use GAIA
- You're running a single model and don't need comparative scores

### How it compares to similar specs
| Instead of THIS | When | Because |
|---|---|---|
| HELM | Academic NLP evaluation | HELM covers broader NLP tasks (sentiment, QA, summarization); this benchmark is scoped to agent coding |
| MLPerf | ML training/inference throughput | MLPerf measures hardware+software stack performance; this measures model task capability |
| GAIA | General agent reasoning | GAIA tests multi-step reasoning with web tools; this focuses on coding and file manipulation tasks |

### What you lose without THIS
- No standard way to compare LLMs on real agent coding tasks
- Model selection becomes guesswork based on vendor marketing or vibes
- No efficiency measurement — models that waste tokens go unpenalized
- No published, reproducible scores to hold providers accountable

## Tasks

| # | Task | What it tests |
|---|------|---------------|
| 1 | File Parse | Navigate a directory tree, read formats |
| 2 | Shell Find | Filesystem search + shell composition |
| 3 | Error Recovery | Detect and fix tool errors autonomously |
| 4 | CSV Stats | Aggregate + filter structured data |
| 5 | Fix Bug | Patch a broken Python function |
| 6 | SQL Query | Write correct queries against real data |
| 7 | Regex Extract | Pattern matching + structured output |
| 8 | Process Monitor | Inspect running processes, parse output |
| 9 | JSON Schema Validate | Validate against schema, report violations |
| 10 | Concurrent Fetch | Parallel HTTP with rate limiting |

## Scoring

- **1.0** — Correct, clean, no intervention needed
- **0.83** — Correct result but verbose/unnecessary steps
- **0.67** — Plausible approach, partial success
- **0.5** — Right direction, wrong result
- **0.33** — Attempted but fundamentally off
- **0.0** — Failed or refused

## Token Budget

All tests run at **1 RB token budget** (approx 40K tokens per task).
This is intentionally tight — it measures efficiency, not just
capability. A model that needs 200K tokens to fix a bug isn't a
practical agent.

## Runner

The benchmark runner is open source at
[github.com/workswithagents/works-with-agents](https://github.com/workswithagents/works-with-agents)
under `skills/mlops/llm-agent-benchmark/`.

## Updates

New models are added as they become available. The benchmark runs
automatically and results are published to this page within minutes.

---

## Examples

Implementation examples for this version:

| Language | File |
|----------|------|
| Python | [agent-coding-benchmark/v1.0.0/python.md](agent-coding-benchmark/v1.0.0/python.md) |
| TypeScript | [agent-coding-benchmark/v1.0.0/typescript.md](agent-coding-benchmark/v1.0.0/typescript.md) |
| cURL | [agent-coding-benchmark/v1.0.0/curl.md](agent-coding-benchmark/v1.0.0/curl.md) |

