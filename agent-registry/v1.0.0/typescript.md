# Agent Registry — TypeScript Example

```typescript
/** Agent Registry v1.0.0 — TypeScript Reference Implementation */
class AgentRegistry {
  constructor(private api: string = "https://workswithagents.dev") {}
  private async post<T>(path: string, body: Record<string,unknown>): Promise<T> {
    const r = await fetch(`${this.api}${path}`, {method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)});
    if(!r.ok) throw new Error(`Error ${r.status}`);
    return r.json() as Promise<T>;
  }
  async register(agentId: string, publicKey: string, capabilities: string[], owner: string, signature: string) {
    return this.post("/v1/registry/register", {agent_id:agentId,public_key:`ed25519:${publicKey}`,capabilities,owner,signature});
  }
  async get(agentId: string) {
    const r = await fetch(`${this.api}/v1/registry/${agentId}`); return r.json();
  }
  async query(capability?: string, status = "active") {
    const p = new URLSearchParams(); if(capability) p.set("capability",capability); if(status) p.set("status",status);
    const r = await fetch(`${this.api}/v1/registry?${p}`); return r.json();
  }
  async suspend(agentId: string, reason: string, initiatedBy: string) {
    return this.post(`/v1/registry/${agentId}/suspend`, {reason,initiated_by:initiatedBy});
  }
  async revoke(agentId: string, reason: string, initiatedBy: string) {
    return this.post(`/v1/registry/${agentId}/revoke`, {reason,initiated_by:initiatedBy,reassign_pending:true});
  }
}

(async () => {
  console.log("=== Agent Registry v1.0.0 ===\n");
  const reg = new AgentRegistry();
  try { const r = await reg.register("deploy-bot-v2","abc123",["deploy:staging"],"admin@example.com","ed25519:sig"); console.log("1. Registered:", (r as any).status); } catch(e) { console.log("1. (offline):", (e as Error).message); }
  try { const a = await reg.get("deploy-bot-v2"); console.log(`2. Lookup: ${(a as any).status}`); } catch { console.log("2. (offline)"); }
  try { const q = await reg.query("deploy:staging"); console.log(`3. Query: ${(q as any).agents?.length} agents`); } catch { console.log("3. (offline)"); }
  console.log("\n=== Complete ===");
})();
```
