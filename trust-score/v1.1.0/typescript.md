# Trust Score — TypeScript Example

```typescript
/** Agent Trust Score v1.0.0 — TypeScript Reference Implementation */

function calculateTrust(successRate: number, pitfalls: number, skillsReuse: number, peerRating: number, uptime: number): number {
  return +(0.30*successRate + 0.20*Math.min(pitfalls/10,1) + 0.20*Math.min(skillsReuse/5,1) + 0.15*(peerRating/5) + 0.15*uptime).toFixed(3);
}
function getTier(score: number): string {
  if(score>=0.80) return "trusted"; if(score>=0.60) return "reliable"; if(score>=0.40) return "learning"; return "untrusted";
}

class TrustScoreClient {
  constructor(private api: string = "https://workswithagents.dev") {}
  private async post<T>(path: string, body: Record<string,unknown>): Promise<T> {
    const r = await fetch(`${this.api}${path}`, {method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)});
    if(!r.ok) throw new Error(`Error ${r.status}`);
    return r.json() as Promise<T>;
  }
  async getScore(agentId: string) { const r = await fetch(`${this.api}/v1/trust/${agentId}`); return r.json(); }
  async listByTier(tier = "trusted") { const r = await fetch(`${this.api}/v1/trust?tier=${tier}`); return r.json(); }
  async getHistory(agentId: string) { const r = await fetch(`${this.api}/v1/trust/${agentId}/history`); return r.json(); }
  async reportMetrics(agentId: string, successRate: number, pitfalls: number, skills: number) {
    return this.post("/v1/trust/report", {agent_id:agentId,success_rate:successRate,pitfalls_contributed:pitfalls,skills_published:skills});
  }
  async rateAgent(from: string, to: string, rating: number) {
    return this.post("/v1/trust/rate", {from_agent:from,to_agent:to,rating});
  }
}

(async () => {
  console.log("=== Trust Score v1.0.0 ===\n");
  const ts = new TrustScoreClient();
  const score = calculateTrust(0.94, 3, 12, 4.2, 0.997);
  console.log(`1. Calculated: ${score} → Tier: ${getTier(score)}`);
  try { await ts.reportMetrics("hermes-spfx-builder",0.94,3,2); console.log("2. Reported"); } catch(e) { console.log("2. (offline)"); }
  try { const s = await ts.getScore("hermes-spfx-builder"); console.log(`3. Score: ${(s as any).score}`); } catch { console.log("3. (offline)"); }
  console.log("\n=== Complete ===");
})();
```
