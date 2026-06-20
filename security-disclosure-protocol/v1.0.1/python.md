# Security Disclosure Protocol — Python Example

```python
"""Security Disclosure Protocol v1.0.1 — Python Reference Implementation"""
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

    def submit_finding(self, **kwargs):
        return self._post("/v1/security-disclosure/submit-finding", kwargs)
    def embargo_finding(self, **kwargs):
        return self._post("/v1/security-disclosure/embargo-finding", kwargs)
    def notify_vendor(self, **kwargs):
        return self._post("/v1/security-disclosure/notify-vendor", kwargs)
    def publish_disclosure(self, **kwargs):
        return self._post("/v1/security-disclosure/publish-disclosure", kwargs)

if __name__ == "__main__":
    c = Client()
    print("===Security Disclosure Protocol v1.0.1 ===\n")
    ops = ['submit_finding', 'embargo_finding', 'notify_vendor', 'publish_disclosure']
    print(f"{len(ops)} operations: {', '.join(ops)}")
    print("\n=== Complete ===")
```
