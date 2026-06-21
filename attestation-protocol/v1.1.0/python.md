# Attestation Protocol — Python Example

```python
"""Attestation Protocol v1.0.0 — Python Reference Implementation"""
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

    def generate_attestation(self, **kwargs):
        return self._post("/v1/attestation/generate-attestation", kwargs)
    def verify_attestation(self, **kwargs):
        return self._post("/v1/attestation/verify-attestation", kwargs)
    def get_chain(self, **kwargs):
        return self._post("/v1/attestation/get-chain", kwargs)

if __name__ == "__main__":
    c = Client()
    print("===Attestation Protocol v1.0.0 ===\n")
    ops = ['generate_attestation', 'verify_attestation', 'get_chain']
    print(f"{len(ops)} operations: {', '.join(ops)}")
    print("\n=== Complete ===")
```
