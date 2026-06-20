# AI Gateway / Policy Enforcement Point — Python Example

```python
"""AI Gateway / Policy Enforcement Point v1.0.0 — Python Reference Implementation"""
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

    def enforce_policy(self, **kwargs):
        return self._post("/v1/gateway/enforce-policy", kwargs)
    def check_rate_limit(self, **kwargs):
        return self._post("/v1/gateway/check-rate-limit", kwargs)
    def audit_request(self, **kwargs):
        return self._post("/v1/gateway/audit-request", kwargs)
    def block_request(self, **kwargs):
        return self._post("/v1/gateway/block-request", kwargs)

if __name__ == "__main__":
    c = Client()
    print("===AI Gateway / Policy Enforcement Point v1.0.0 ===\n")
    ops = ['enforce_policy', 'check_rate_limit', 'audit_request', 'block_request']
    print(f"{len(ops)} operations: {', '.join(ops)}")
    print("\n=== Complete ===")
```
