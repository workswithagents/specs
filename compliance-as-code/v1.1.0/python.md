# Compliance-as-Code — Python Example

```python
"""Compliance-as-Code v1.0.0 — Python Reference Implementation"""
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

    def validate_rules(self, **kwargs):
        return self._post("/v1/compliance/validate-rules", kwargs)
    def check_compliance(self, **kwargs):
        return self._post("/v1/compliance/check-compliance", kwargs)
    def run_audit(self, **kwargs):
        return self._post("/v1/compliance/run-audit", kwargs)
    def generate_report(self, **kwargs):
        return self._post("/v1/compliance/generate-report", kwargs)

if __name__ == "__main__":
    c = Client()
    print("===Compliance-as-Code v1.0.0 ===\n")
    ops = ['validate_rules', 'check_compliance', 'run_audit', 'generate_report']
    print(f"{len(ops)} operations: {', '.join(ops)}")
    print("\n=== Complete ===")
```
