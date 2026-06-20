# Trust Score — Python Example

```python
"""Agent Trust Score v1.0.0 — Python Reference Implementation"""
import json, urllib.request, urllib.error

class TrustScoreClient:
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

    def get_score(self, agent_id: str):
        return self._get(f"/v1/trust/{agent_id}")

    def list_by_tier(self, tier: str = "trusted"):
        return self._get(f"/v1/trust?tier={tier}")

    def get_history(self, agent_id: str):
        return self._get(f"/v1/trust/{agent_id}/history")

    def report_metrics(self, agent_id: str, success_rate: float, pitfalls_contributed: int, skills_published: int):
        return self._post("/v1/trust/report", {"agent_id":agent_id,"success_rate":success_rate,"pitfalls_contributed":pitfalls_contributed,"skills_published":skills_published})

    def rate_agent(self, from_agent: str, to_agent: str, rating: float):
        return self._post("/v1/trust/rate", {"from_agent":from_agent,"to_agent":to_agent,"rating":rating})

def calculate_trust(success_rate, pitfalls, skills_reuse, peer_rating, uptime):
    return round(0.30*success_rate + 0.20*min(pitfalls/10,1.0) + 0.20*min(skills_reuse/5,1.0) + 0.15*(peer_rating/5) + 0.15*uptime, 3)

def get_tier(score):
    if score >= 0.80: return "trusted"
    elif score >= 0.60: return "reliable"
    elif score >= 0.40: return "learning"
    return "untrusted"

if __name__ == "__main__":
    ts = TrustScoreClient()
    print("=== Trust Score v1.0.0 ===\n")
    score = calculate_trust(0.94, 3, 12, 4.2, 0.997)
    print(f"1. Calculated trust: {score} → Tier: {get_tier(score)}")
    try:
        r = ts.report_metrics("hermes-spfx-builder", 0.94, 3, 2)
        print(f"2. Reported metrics: {r.get('status','ok')}")
    except: print("2. Report (offline)")
    try:
        s = ts.get_score("hermes-spfx-builder")
        print(f"3. Score: {s.get('score')}, Tier: {s.get('tier')}")
    except: print("3. Get (offline)")
    try:
        trusted = ts.list_by_tier("trusted")
        print(f"4. Trusted agents: {len(trusted)}")
    except: print("4. List (offline)")
    try:
        ts.rate_agent("builder-01", "reviewer-02", 4.5)
        print("5. Rated reviewer-02: 4.5/5")
    except: print("5. Rate (offline)")
    print("\n=== Complete ===")
```
