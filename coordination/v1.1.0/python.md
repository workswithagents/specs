# Coordination Protocol (ACP) — Python Example

```python
"""Coordination Protocol (ACP) v1.0.0 — Python Reference Implementation"""
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

    def elect_leader(self, **kwargs):
        return self._post("/v1/coordination/elect-leader", kwargs)
    def distribute_work(self, **kwargs):
        return self._post("/v1/coordination/distribute-work", kwargs)
    def steal_work(self, **kwargs):
        return self._post("/v1/coordination/steal-work", kwargs)
    def heartbeat(self, **kwargs):
        return self._post("/v1/coordination/heartbeat", kwargs)

if __name__ == "__main__":
    c = Client()
    print("===Coordination Protocol (ACP) v1.0.0 ===\n")
    ops = ['elect_leader', 'distribute_work', 'steal_work', 'heartbeat']
    print(f"{len(ops)} operations: {', '.join(ops)}")
    print("\n=== Complete ===")
```
