# Holistic Evaluation of Language Models (HELM)

**Version:** latest
**Status:** Published
**Layer:** L6 — Verification
**Steward:** Stanford CRFM
**License:** Academic
**Website:** https://crfm.stanford.edu/helm/
**Repository:** https://github.com/stanford-crfm/helm

## Relationship to WWA

HELM is a comprehensive LLM evaluation framework operating at the verification layer (L6). WWA's benchmarks (Agent Coding Benchmark, Agent Economics) are agent-specific, evaluating what agents do with models. HELM evaluates the models themselves across multiple dimensions: accuracy, calibration, robustness, fairness, bias, toxicity, and efficiency. The two are complementary — HELM classifies which models are suitable foundation candidates, while WWA benchmarks assess how well those models perform when deployed as agents with tool access and coordination protocols. A WWA agent might use HELM scores to select the best model for a given task type.

## Architecture

HELM evaluates models by running them through standardized **scenarios** — task formulations drawn from existing benchmarks (MMLU, TruthfulQA, GSM8K, etc.) reformatted into a consistent input/output interface. Each scenario is evaluated across multiple **metrics** (7 categories: accuracy, calibration, robustness, fairness, bias, toxicity, efficiency). Results are aggregated into a public leaderboard with per-model, per-metric comparisons. The framework supports hundreds of models via API integration (OpenAI, Anthropic, Google, etc.) and local inference. HELM is implemented in Python with a modular adapter architecture.

## Features

- Multi-metric evaluation: accuracy, calibration, robustness, fairness, bias, toxicity, efficiency
- Standardized scenarios: unified interface over 40+ existing benchmarks
- Public leaderboard with interactive visualizations
- Comprehensive model coverage (200+ models evaluated)
- Extensible: new scenarios and metrics can be added
- Python framework with CLI and programmatic APIs
- Academic research-grade methodology (Stanford CRFM)

## Governance

Developed and maintained by the Stanford Center for Research on Foundation Models (CRFM), an academic research group. HELM is an academic research framework, not a commercial product. The codebase is open-source (Apache 2.0) and available on GitHub. Updates are driven by ongoing research at Stanford, with results published in academic papers. The leaderboard is updated periodically as new models are released.

## Examples

Implementation examples for this version:

| Language | File |
|----------|------|
| Python | [related-helm/v1.0.0/python.md](related-helm/v1.0.0/python.md) |
