# IACP Internet Draft — Python Example

```python
"""IACP Internet Draft vdraft-00 — Python Reference Implementation"""
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

    def discover_peers(self, **kwargs):
        return self._post("/v1/iacp/discover-peers", kwargs)
    def send_message(self, **kwargs):
        return self._post("/v1/iacp/send-message", kwargs)
    def poll_inbox(self, **kwargs):
        return self._post("/v1/iacp/poll-inbox", kwargs)
    def heartbeat(self, **kwargs):
        return self._post("/v1/iacp/heartbeat", kwargs)

if __name__ == "__main__":
    c = Client()
    print("===IACP Internet Draft vdraft-00 ===\n")
    ops = ['discover_peers', 'send_message', 'poll_inbox', 'heartbeat']
    print(f"{len(ops)} operations: {', '.join(ops)}")
    print("\n=== Complete ===")
```
