# AP2 Payment Mandate — Python Example

```python
"""AP2 Payment Mandate v0.9.0 — Python Reference Implementation"""
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

    def create_mandate(self, **kwargs):
        return self._post("/v1/ap2/create-mandate", kwargs)
    def verify_spend(self, **kwargs):
        return self._post("/v1/ap2/verify-spend", kwargs)
    def revoke_mandate(self, **kwargs):
        return self._post("/v1/ap2/revoke-mandate", kwargs)
    def get_spend_history(self, **kwargs):
        return self._post("/v1/ap2/get-spend-history", kwargs)

if __name__ == "__main__":
    c = Client()
    print("===AP2 Payment Mandate v0.9.0 ===\n")
    ops = ['create_mandate', 'verify_spend', 'revoke_mandate', 'get_spend_history']
    print(f"{len(ops)} operations: {', '.join(ops)}")
    print("\n=== Complete ===")
```
