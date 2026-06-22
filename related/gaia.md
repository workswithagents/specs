# GAIA — General AI Assistants Benchmark

**Version:** latest
**Status:** Published
**Layer:** L6 — Verification
**Steward:** Meta FAIR / Hugging Face
**License:** MIT (benchmark)
**Website:** https://huggingface.co/gaia-benchmark
**Repository:** https://huggingface.co/datasets/gaia-benchmark/GAIA

## Relationship to WWA

GAIA is an academic agent evaluation benchmark operating at the verification layer (L6). WWA's Agent Coding Benchmark focuses specifically on coding tasks (SWE-bench style, bug fixes, feature implementation). GAIA covers broader general assistant capabilities: web browsing, tool use, multi-step reasoning, and information synthesis. The two benchmarks are complementary — GAIA evaluates whether an agent can navigate the web and reason about real-world information, while WWA evaluates whether an agent can produce correct, working code. Together they provide a more complete picture of agent capability than either alone.

### Problem

Most AI benchmarks evaluate narrow capabilities — code generation, math, or question answering — but real-world agent tasks require chaining multiple skills: searching the web, extracting data from pages, performing calculations, and synthesizing results. Without a benchmark that tests this multi-step, tool-using behavior, it's impossible to know whether an agent can actually function as a general-purpose assistant rather than a single-skill tool.

### Solution

GAIA provides 466 carefully crafted questions that require agents to navigate the web, use tools, and perform multi-step reasoning — tasks that are trivial for humans but challenging for AI. Questions are graded across three difficulty levels: L1 (1-2 tool calls), L2 (3-5 steps across multiple tools), and L3 (5+ steps requiring adaptive strategies). The public Hugging Face leaderboard tracks progress, giving researchers and developers a shared yardstick for general agent capability.

### When to use

- Evaluating general-purpose agent architectures beyond coding benchmarks
- Research comparing agent frameworks on real-world reasoning and tool-use tasks
- Selecting an agent framework for deployment by validating its general reasoning capabilities
- Academic benchmarking where a public leaderboard and peer comparison are valuable

### When NOT to use

- Evaluating an agent's coding-specific capabilities — use WWA Agent Coding Benchmark for SWE-bench-style tasks
- Model-level evaluation without tool use — use HELM for raw LLM capability assessment
- Performance benchmarking (inference speed, throughput) — use MLPerf for system-level metrics
- Continuous integration testing — GAIA is a research benchmark, not a CI pipeline tool

### How it compares to similar specs

| Instead of THIS spec | When | Because |
|---|---|---|
| WWA Agent Coding Benchmark | Evaluating coding agent performance on software engineering tasks | WWA's benchmark focuses specifically on code generation, debugging, and refactoring |
| HELM | Evaluating raw LLM capabilities without tool use | HELM measures model accuracy, calibration, and bias across 40+ benchmarks without agent scaffolding |
| MLPerf | Benchmarking ML system performance (throughput, latency) | MLPerf evaluates hardware and inference infrastructure, not agent reasoning quality |

### What you lose without THIS spec

- No standard benchmark for general-purpose agent reasoning and web-based tool use
- Cannot compare agent architectures on multi-step, real-world assistant tasks
- Risk of over-fitting to coding benchmarks, missing weaknesses in web navigation and information synthesis
- No shared leaderboard for tracking industry-wide progress on general agent capabilities

## Architecture

GAIA consists of 466 carefully crafted questions across three difficulty levels (L1, L2, L3). Questions require agents to perform multi-step reasoning that is trivial for humans but challenging for AI — for example, navigating a website, extracting specific data, and performing calculations. L1 questions typically involve 1-2 tool calls (simple web search or file read). L2 questions require 3-5 steps and multiple tool types. L3 questions demand complex, adaptive strategies of 5+ steps. The benchmark is hosted on Hugging Face, with a public leaderboard tracking agent performance across submissions.

## Features

- 466 curated questions across three difficulty levels (L1, L2, L3)
- Multi-step reasoning requiring tool use and web browsing
- Questions designed to be easy for humans, hard for AI
- Public leaderboard on Hugging Face
- Evaluation via exact match and normalized answers
- Open-source dataset under MIT license
- Used by major AI labs for agent capability benchmarking

## Governance

Created by researchers at Meta FAIR, Hugging Face, and collaborating institutions. The benchmark dataset is MIT-licensed and hosted on Hugging Face. It is an academic research benchmark — an evaluation dataset, not a protocol or framework. The leaderboard is maintained by the GAIA team, with community submissions accepted through Hugging Face.

> **Note:** GAIA is a benchmark dataset, not a protocol or software framework. It defines evaluation questions and scoring methodology. No canonical code examples exist — implementation is left to agent developers who submit their results.
