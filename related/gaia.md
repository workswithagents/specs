# GAIA — General AI Assistants Benchmark

**Version:** 1.0
**Status:** Published
**Layer:** L6 — Verification
**Steward:** Meta FAIR / Hugging Face
**License:** MIT (benchmark)
**Website:** https://huggingface.co/gaia-benchmark
**Repository:** https://huggingface.co/datasets/gaia-benchmark/GAIA

## Relationship to WWA

GAIA is an academic agent evaluation benchmark operating at the verification layer (L6). WWA's Agent Coding Benchmark focuses specifically on coding tasks (SWE-bench style, bug fixes, feature implementation). GAIA covers broader general assistant capabilities: web browsing, tool use, multi-step reasoning, and information synthesis. The two benchmarks are complementary — GAIA evaluates whether an agent can navigate the web and reason about real-world information, while WWA evaluates whether an agent can produce correct, working code. Together they provide a more complete picture of agent capability than either alone.

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
