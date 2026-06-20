# Transaction Protocol (ATP) — Python Example

```python
"""Transaction Protocol (ATP) v1.0.0 — Python Reference Implementation"""
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

    def create_transaction(self, **kwargs):
        return self._post("/v1/transaction/create-transaction", kwargs)
    def commit(self, **kwargs):
        return self._post("/v1/transaction/commit", kwargs)
    def rollback(self, **kwargs):
        return self._post("/v1/transaction/rollback", kwargs)
    def get_status(self, **kwargs):
        return self._post("/v1/transaction/get-status", kwargs)

if __name__ == "__main__":
    c = Client()
    print("===Transaction Protocol (ATP) v1.0.0 ===\n")
    ops = ['create_transaction', 'commit', 'rollback', 'get_status']
    print(f"{len(ops)} operations: {', '.join(ops)}")
    print("\n=== Complete ===")
```
