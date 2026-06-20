# Local-First Certification — Python Example

```python
"""Local-First Certification v1.0.0 — Python Reference Implementation"""
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

    def validate_certification(self, **kwargs):
        return self._post("/v1/local-first/validate-certification", kwargs)
    def check_offline(self, **kwargs):
        return self._post("/v1/local-first/check-offline", kwargs)
    def audit_external_calls(self, **kwargs):
        return self._post("/v1/local-first/audit-external-calls", kwargs)

if __name__ == "__main__":
    c = Client()
    print("===Local-First Certification v1.0.0 ===\n")
    ops = ['validate_certification', 'check_offline', 'audit_external_calls']
    print(f"{len(ops)} operations: {', '.join(ops)}")
    print("\n=== Complete ===")
```
