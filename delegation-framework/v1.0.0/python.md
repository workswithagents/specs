# Delegation Framework — Python Example

```python
"""Delegation Framework v1.0.0 — Python Reference Implementation"""
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

    def issue_delegation(self, **kwargs):
        return self._post("/v1/delegation/issue-delegation", kwargs)
    def verify_delegation(self, **kwargs):
        return self._post("/v1/delegation/verify-delegation", kwargs)
    def revoke_delegation(self, **kwargs):
        return self._post("/v1/delegation/revoke-delegation", kwargs)
    def list_delegations(self, **kwargs):
        return self._post("/v1/delegation/list-delegations", kwargs)

if __name__ == "__main__":
    c = Client()
    print("===Delegation Framework v1.0.0 ===\n")
    ops = ['issue_delegation', 'verify_delegation', 'revoke_delegation', 'list_delegations']
    print(f"{len(ops)} operations: {', '.join(ops)}")
    print("\n=== Complete ===")
```
