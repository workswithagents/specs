# Agent Coding Benchmark — Python Example

```python
"""Agent Coding Benchmark v1.0.0 — Python Reference Implementation"""
import json, urllib.request, urllib.error

class Client:
    def __init__(self, api: str = "https://workswithagents.dev"):
        self.api = api.rstrip("/")
    def _post(self, path, body):
        d = json.dumps(body).encode()
        r = urllib.request.Request(f"{self.api}{path}", data=d, method="POST", headers={"Content-Type":"application/json"})
        try:
            with urllib.request.urlopen(r) as resp: return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"Error {e.code}: {json.loads(e.read()).get('detail')}")
    def _get(self, path):
        with urllib.request.urlopen(f"{self.api}{path}") as r: return json.loads(r.read())

    def run_benchmark(self, **kwargs):
        return self._post("/v1/benchmark/run-benchmark", kwargs)
    def get_results(self, **kwargs):
        return self._post("/v1/benchmark/get-results", kwargs)
    def compare_models(self, **kwargs):
        return self._post("/v1/benchmark/compare-models", kwargs)

if __name__ == "__main__":
    c = Client()
    print("===Agent Coding Benchmark v1.0.0 ===\n")
    ops = ['run_benchmark', 'get_results', 'compare_models']
    print(f"{len(ops)} operations: {', '.join(ops)}")
    print("\n=== Complete ===")
```
