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
