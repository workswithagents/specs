# MLPerf

**Version:** 5.1.1
**Status:** Published
**Layer:** L6 — Verification
**Steward:** MLCommons
**License:** Open standard
**Website:** https://mlcommons.org/
**Repository:** https://github.com/mlcommons

## Relationship to WWA

MLPerf is the industry-standard benchmark suite for ML system performance, operating at the verification layer (L6). WWA's Agent Coding Benchmark is more specialized — it evaluates agent performance on software engineering tasks (code generation, debugging, refactoring). MLPerf covers a different scope: model training throughput, inference latency, and HPC performance. The two are complementary: MLPerf evaluates the underlying model infrastructure, WWA benchmarks evaluate the agent's task-completion capabilities. An agent's overall performance depends on both the model quality (measured by MLPerf-style benchmarks) and the agent protocol efficiency (measured by WWA benchmarks).

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
