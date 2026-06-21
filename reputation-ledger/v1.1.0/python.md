# Reputation Ledger — Python Example

```python
"""Reputation Ledger v1.0.0 — Python Reference Implementation"""
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

    def record_claim(self, **kwargs):
        return self._post("/v1/reputation/record-claim", kwargs)
    def verify_claim(self, **kwargs):
        return self._post("/v1/reputation/verify-claim", kwargs)
    def get_reputation(self, **kwargs):
        return self._post("/v1/reputation/get-reputation", kwargs)
    def challenge_claim(self, **kwargs):
        return self._post("/v1/reputation/challenge-claim", kwargs)

if __name__ == "__main__":
    c = Client()
    print("===Reputation Ledger v1.0.0 ===\n")
    ops = ['record_claim', 'verify_claim', 'get_reputation', 'challenge_claim']
    print(f"{len(ops)} operations: {', '.join(ops)}")
    print("\n=== Complete ===")
```
