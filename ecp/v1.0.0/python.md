# Ephemeral Communication Protocol — Python Example

```python
"""Ephemeral Communication Protocol v1.0.0 — Python Reference Implementation"""
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

    def create_room(self, **kwargs):
        return self._post("/v1/ecp/create-room", kwargs)
    def send_message(self, **kwargs):
        return self._post("/v1/ecp/send-message", kwargs)
    def destroy_room(self, **kwargs):
        return self._post("/v1/ecp/destroy-room", kwargs)
    def get_ttl(self, **kwargs):
        return self._post("/v1/ecp/get-ttl", kwargs)

if __name__ == "__main__":
    c = Client()
    print("===Ephemeral Communication Protocol v1.0.0 ===\n")
    ops = ['create_room', 'send_message', 'destroy_room', 'get_ttl']
    print(f"{len(ops)} operations: {', '.join(ops)}")
    print("\n=== Complete ===")
```
