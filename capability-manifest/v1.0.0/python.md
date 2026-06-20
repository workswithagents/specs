# Capability Manifest — Python Example

```python
"""Capability Manifest v1.0.0 — Python Reference Implementation"""
import json, time, urllib.request, urllib.error
from typing import Optional

class CapabilityManifest:
    """Agent capability declaration and registry client."""
    def __init__(self, agent_id: str, api: str = "https://workswithagents.dev"):
        self.agent_id = agent_id; self.api = api.rstrip("/")

    def _post(self, path, body):
        d = json.dumps(body).encode()
        r = urllib.request.Request(f"{self.api}{path}", data=d, method="POST",
            headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(r) as resp: return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"Error {e.code}: {json.loads(e.read()).get('detail')}")

    def _get(self, path):
        with urllib.request.urlopen(f"{self.api}{path}") as r: return json.loads(r.read())

    def register(self, capabilities: list, tools: list, endpoint: str):
        return self._post("/v1/agents/register", {
            "manifest_version": "1.0.0", "agent_id": self.agent_id,
            "capabilities": capabilities, "tools": tools,
            "endpoint": {"address": endpoint, "protocol": "acp"},
            "status": {"state": "healthy", "load": 0.0, "current_tasks": 0, "max_tasks": 3}
        })

    def heartbeat(self, load: float, current_tasks: int, status: str = "healthy"):
        return self._post(f"/v1/agents/{self.agent_id}/heartbeat",
            {"load": load, "current_tasks": current_tasks, "state": status,
             "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})

    def query(self, action: Optional[str] = None, target: Optional[str] = None):
        path = "/v1/agents"
        params = []
        if action: params.append(f"action={action}")
        if target: params.append(f"target={target}")
        if params: path += "?" + "&".join(params)
        return self._get(path)

    def deregister(self):
        req = urllib.request.Request(f"{self.api}/v1/agents/{self.agent_id}", method="DELETE")
        with urllib.request.urlopen(req) as r: return r.status

if __name__ == "__main__":
    agent = CapabilityManifest("hermes-spfx-builder")
    print("=== Capability Manifest v1.0.0 ===\n")
    try:
        r = agent.register(
            capabilities=[{"action": "build", "target": "spfx", "success_rate": 0.94, "avg_duration_seconds": 180}],
            tools=["node", "gulp", "npm"], endpoint="agent://spfx-builder:8782")
        print(f"1. Registered: {r.get('status', 'active')}")
    except RuntimeError as e: print(f"1. (offline): {e}")
    try:
        hb = agent.heartbeat(load=0.67, current_tasks=2)
        print(f"2. Heartbeat sent: load={0.67}")
    except: print("2. Heartbeat (offline)")
    try:
        agents = agent.query(action="build", target="spfx")
        print(f"3. Query: found {len(agents.get('agents',[]))} agent(s)")
        if agents.get("recommended"): print(f"   Recommended: {agents['recommended']}")
    except: print("3. Query (offline)")
    print("\n=== Complete ===")
```
