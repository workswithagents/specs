# Agent Registry — Python Example

```python
"""Agent Registry v1.0.0 — Python Reference Implementation"""
import json, urllib.request, urllib.error

class AgentRegistry:
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

    def register(self, agent_id: str, public_key: str, capabilities: list, owner: str, signature: str):
        return self._post("/v1/registry/register", {"agent_id":agent_id,"public_key":f"ed25519:{public_key}","capabilities":capabilities,"owner":owner,"signature":signature})

    def get(self, agent_id: str):
        return self._get(f"/v1/registry/{agent_id}")

    def query(self, capability: str = None, status: str = "active"):
        path = "/v1/registry"
        params = []
        if capability: params.append(f"capability={urllib.request.quote(capability)}")
        if status: params.append(f"status={status}")
        if params: path += "?" + "&".join(params)
        return self._get(path)

    def update_capabilities(self, agent_id: str, capabilities: list, signature: str):
        return self._post(f"/v1/registry/{agent_id}/capabilities", {"capabilities":capabilities,"signature":signature})

    def suspend(self, agent_id: str, reason: str, initiated_by: str):
        return self._post(f"/v1/registry/{agent_id}/suspend", {"reason":reason,"initiated_by":initiated_by})

    def revoke(self, agent_id: str, reason: str, initiated_by: str, reassign: bool = True):
        return self._post(f"/v1/registry/{agent_id}/revoke", {"reason":reason,"initiated_by":initiated_by,"reassign_pending":reassign})

    def audit_log(self, agent_id: str):
        return self._get(f"/v1/registry/{agent_id}/audit")

if __name__ == "__main__":
    reg = AgentRegistry()
    print("=== Agent Registry v1.0.0 ===\n")
    try:
        r = reg.register("deploy-bot-v2", "abc123def456", ["deploy:staging", "deploy:production"], "admin@example.com", "ed25519:sig...")
        print(f"1. Registered: {r.get('status')}")
    except RuntimeError as e: print(f"1. (offline): {e}")
    try:
        agent = reg.get("deploy-bot-v2")
        print(f"2. Lookup: status={agent.get('status')}, capabilities={agent.get('capabilities')}")
    except: print("2. Lookup (offline)")
    try:
        agents = reg.query(capability="deploy:staging")
        print(f"3. Query: {len(agents.get('agents',[]))} agents with deploy:staging")
    except: print("3. Query (offline)")
    try:
        reg.suspend("deploy-bot-v2", "security review", "admin@example.com")
        print("4. Suspended")
    except: print("4. Suspend (offline)")
    try:
        reg.revoke("deploy-bot-v2", "compromised", "admin@example.com")
        print("5. Revoked")
    except: print("5. Revoke (offline)")
    print("\n=== Complete ===")
```
