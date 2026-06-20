# IACP Fault Tolerance — Python Example

```python
"""IACP Fault Tolerance v1.0.0 — Python Reference Implementation"""
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

    def detect_timeout(self, **kwargs):
        return self._post("/v1/iacp/fault-tolerance/detect-timeout", kwargs)
    def handle_dead_letter(self, **kwargs):
        return self._post("/v1/iacp/fault-tolerance/handle-dead-letter", kwargs)
    def rollback(self, **kwargs):
        return self._post("/v1/iacp/fault-tolerance/rollback", kwargs)
    def retry_with_backoff(self, **kwargs):
        return self._post("/v1/iacp/fault-tolerance/retry-with-backoff", kwargs)

if __name__ == "__main__":
    c = Client()
    print("===IACP Fault Tolerance v1.0.0 ===\n")
    ops = ['detect_timeout', 'handle_dead_letter', 'rollback', 'retry_with_backoff']
    print(f"{len(ops)} operations: {', '.join(ops)}")
    print("\n=== Complete ===")
```
