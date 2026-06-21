# Clarification Protocol — Python Example

```python
"""Clarification Protocol v1.0.0 — Python Reference Implementation"""
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

    def submit_clarification(self, **kwargs):
        return self._post("/v1/clarification/submit-clarification", kwargs)
    def resolve_gap(self, **kwargs):
        return self._post("/v1/clarification/resolve-gap", kwargs)
    def list_gaps(self, **kwargs):
        return self._post("/v1/clarification/list-gaps", kwargs)
    def session_status(self, **kwargs):
        return self._post("/v1/clarification/session-status", kwargs)

if __name__ == "__main__":
    c = Client()
    print("===Clarification Protocol v1.0.0 ===\n")
    ops = ['submit_clarification', 'resolve_gap', 'list_gaps', 'session_status']
    print(f"{len(ops)} operations: {', '.join(ops)}")
    print("\n=== Complete ===")
```
