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

### Problem

Choosing a foundation model for an agent is a multi-dimensional decision — a model that scores high on accuracy might be poorly calibrated, or a model that's fast might be biased against certain demographic groups. Most benchmarks evaluate a single dimension (accuracy on MMLU, reasoning on GSM8K), leaving developers to stitch together results from disparate sources. Without a holistic view, model selection becomes guesswork rather than engineering.

### Solution

HELM evaluates models across seven metric categories — accuracy, calibration, robustness, fairness, bias, toxicity, and efficiency — using a standardized interface over 40+ existing benchmarks. Every model runs through the same scenarios and metrics, producing comparable scores across all dimensions. The public leaderboard lets developers see not just which model is "best" but which model is best for their specific tradeoffs: accuracy vs. latency, robustness vs. cost, fairness vs. raw capability.

### When to use

- Selecting a foundation model for an agent deployment when multiple dimensions matter
- Research comparing LLM architectures across fairness, robustness, and calibration (not just accuracy)
- Pre-deployment due diligence — checking a model's bias and toxicity scores before exposing it to users
- Academic research requiring rigorous, reproducible model evaluation methodology

### When NOT to use

- Evaluating agent-specific coding performance — use WWA Agent Coding Benchmark for coding tasks with tool access
- Simple accuracy-only model comparison — a single benchmark like MMLU is faster and sufficient
- Production throughput/latency benchmarking — use MLPerf Inference for system-level performance metrics
- Continuous integration model regression testing — HELM is a comprehensive research framework, not a CI tool

### How it compares to similar specs

| Instead of THIS spec | When | Because |
|---|---|---|
| WWA Agent Coding Benchmark | Evaluating agent coding performance with tools | WWA's benchmark tests agent + tool combinations, not raw model capability |
| GAIA | Evaluating general-purpose agent reasoning and web tool use | GAIA tests agent scaffolding, not the underlying model in isolation |
| MLPerf | Benchmarking training throughput or inference latency | MLPerf evaluates hardware/system performance, not model quality across dimensions |

### What you lose without THIS spec

- No standardized, multi-dimensional model evaluation across accuracy, calibration, fairness, bias, toxicity, and efficiency
- Model selection is based on single-metric benchmarks (e.g., MMLU accuracy alone), ignoring critical dimensions like robustness
- No way to compare models on fairness or toxicity without running separate, incompatible evaluations
- Stanford CRFM's rigorous academic methodology for reproducible model evaluation

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

### Python
```python
from helm.benchmark.runner import run_benchmarking
from helm.common.authentication import Authentication
from helm.common.request import Request, RequestResult

# Run a single evaluation
request = Request(
    model="openai/gpt-4o",
    prompt="What is the capital of France?",
    temperature=0.0,
    max_tokens=10,
)

# Run a full benchmark suite
results = run_benchmarking(
    models=["openai/gpt-4o", "anthropic/claude-3-5-sonnet"],
    scenarios=["mmlu", "truthful_qa", "gsm8k"],
    metrics=["accuracy", "calibration", "robustness"],
    max_instances=100,
    output_path="./helm-results",
)

# Analyze results
for model_result in results:
    print(f"Model: {model_result.model}")
    for metric in model_result.metrics:
        print(f"  {metric.name}: {metric.value:.3f}")
```

### CLI
```bash
# Run HELM evaluation from the command line
helm-run \
  --run-specs "mmlu:model=openai/gpt-4o,model=anthropic/claude-3-5-sonnet" \
  --max-eval-instances 100 \
  --suite v1 \
  --output-path ./helm-results

# Summarize results
helm-summarize --suite v1 --output-path ./helm-results
```
