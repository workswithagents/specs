# MLPerf

**Version:** latest
**Status:** Published
**Layer:** L6 — Verification
**Steward:** MLCommons
**License:** Open standard
**Website:** https://mlcommons.org/
**Repository:** https://github.com/mlcommons

## Relationship to WWA

MLPerf is the industry-standard benchmark suite for ML system performance, operating at the verification layer (L6). WWA's Agent Coding Benchmark is more specialized — it evaluates agent performance on software engineering tasks (code generation, debugging, refactoring). MLPerf covers a different scope: model training throughput, inference latency, and HPC performance. The two are complementary: MLPerf evaluates the underlying model infrastructure, WWA benchmarks evaluate the agent's task-completion capabilities. An agent's overall performance depends on both the model quality (measured by MLPerf-style benchmarks) and the agent protocol efficiency (measured by WWA benchmarks).

### Problem

ML hardware and software vendors publish performance claims using wildly different methodologies — one vendor's "throughput" number uses batch size 1, another uses batch size 256; one measures end-to-end latency, another measures only model execution time. Without a standardized, peer-reviewed benchmark suite, comparing GPU A to GPU B or framework X to framework Y is marketing theater, not engineering. Buyers cannot make informed infrastructure decisions.

### Solution

MLPerf defines rigorous, reproducible benchmark suites across Training, Inference, HPC, and Tiny (edge/IoT) workloads. Every submission follows strict rules for hardware, software, and methodology, and results are peer-reviewed before publication. The MLCommons consortium (70+ member organizations including NVIDIA, Intel, Google, and AMD) governs the standard, ensuring no single vendor controls the rules. The public leaderboard provides transparent, apples-to-apples comparisons.

### When to use

- Comparing hardware platforms (GPUs, TPUs, accelerators) for ML training or inference workloads
- Optimizing inference serving infrastructure — understanding latency/throughput tradeoffs under standardized conditions
- Vendor evaluation for large-scale ML infrastructure purchases
- Publishing reproducible ML performance research

### When NOT to use

- Evaluating agent coding or reasoning quality — use WWA Agent Coding Benchmark or GAIA for agent task performance
- Evaluating model accuracy or bias — use HELM for multi-dimensional LLM quality assessment
- Quick, informal performance checks — MLPerf submission is a heavy process; use simple benchmarks for development iteration
- Edge cases not covered by standard MLPerf workloads — MLPerf covers common scenarios, not every custom model architecture

### How it compares to similar specs

| Instead of THIS spec | When | Because |
|---|---|---|
| WWA Agent Coding Benchmark | Evaluating agent coding task completion | WWA benchmarks agent capability, not hardware throughput |
| HELM | Evaluating LLM quality across accuracy, fairness, bias | HELM measures what the model knows; MLPerf measures how fast it runs |
| GAIA | Evaluating agent reasoning and tool-use capability | GAIA tests multi-step agent behavior, not system-level ML performance |

### What you lose without THIS spec

- No industry-standard, peer-reviewed ML performance benchmark — every comparison uses incompatible methodologies
- Cannot make informed hardware purchasing decisions with confidence in vendor claims
- No standard for measuring ML training time-to-convergence or inference serving throughput
- 70+ member consortium governance ensuring no single vendor controls the benchmark rules

## Architecture

MLPerf is organized into benchmark suites: Training (time-to-train models like ResNet, BERT, GPT-3), Inference (latency and throughput for serving), HPC (high-performance computing workloads), and Tiny (edge/IoT devices). Results are submitted by participating organizations, peer-reviewed, and published on the MLCommons leaderboard. Each suite defines strict rules for hardware, software, and methodology to ensure reproducible comparisons. MLPerf does not provide code — it provides benchmark definitions, rules, and a results repository.

## Features

- Training benchmarks: time-to-train across computer vision, NLP, recommendation, and more
- Inference benchmarks: latency and throughput in datacenter, edge, mobile, and tiny scenarios
- HPC benchmarks: coupled scientific simulations with ML (CosmoFlow, DeepCAM)
- Tiny benchmarks: ultra-low-power inference for IoT and embedded devices
- Peer-reviewed results with public leaderboard
- Multi-vendor participation (NVIDIA, Intel, Google, AMD, and 70+ members)

## Governance

Governed by MLCommons, a non-profit industry consortium with over 70 member organizations. MLCommons uses working groups for each benchmark suite, with members contributing to benchmark design and reviewing results. MLPerf is an open standard — specifications and rules are publicly available, and anyone can submit results. This is an industry consortium standard, not a source-code project. No code examples are part of the specification.

> **Note:** MLPerf is a benchmark standard, not a software project. It defines evaluation methodology and results reporting. There are no canonical code examples — implementations are provided by individual submitters.
