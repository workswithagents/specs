# Capability Manifest — TypeScript Example

```typescript
/** Capability Manifest v1.0.0 — TypeScript Reference Implementation */
interface Capability { action: string; target: string; success_rate: number; avg_duration_seconds: number; }
interface AgentStatus { state: string; load: number; current_tasks: number; max_tasks: number; }

class CapabilityManifest {
  constructor(private agentId: string, private api: string = "https://workswithagents.dev") {}
  private async post<T>(path: string, body: Record<string,unknown>): Promise<T> {
    const r = await fetch(`${this.api}${path}`, {method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)});
    if(!r.ok) throw new Error(`Error ${r.status}`);
    return r.json() as Promise<T>;
  }
  async register(capabilities: Capability[], tools: string[], endpoint: string) {
    return this.post("/v1/agents/register", {manifest_version:"1.0.0",agent_id:this.agentId,capabilities,tools,endpoint:{address:endpoint,protocol:"acp"},status:{state:"healthy",load:0,current_tasks:0,max_tasks:3}});
  }
  async heartbeat(load: number, currentTasks: number, state = "healthy") {
    return this.post(`/v1/agents/${this.agentId}/heartbeat`, {load,current_tasks:currentTasks,state,timestamp:new Date().toISOString()});
  }
  async query(action?: string, target?: string) {
    const params = new URLSearchParams(); if(action) params.set("action",action); if(target) params.set("target",target);
    const r = await fetch(`${this.api}/v1/agents?${params}`); return r.json();
  }
  async deregister() { await fetch(`${this.api}/v1/agents/${this.agentId}`, {method:"DELETE"}); }
}

(async () => {
  console.log("=== Capability Manifest v1.0.0 ===\n");
  const agent = new CapabilityManifest("hermes-spfx-builder");
  try { const r = await agent.register([{action:"build",target:"spfx",success_rate:0.94,avg_duration_seconds:180}],["node","gulp","npm"],"agent://spfx-builder:8782"); console.log("1. Registered:", (r as any).status); } catch(e) { console.log("1. (offline):", (e as Error).message); }
  try { await agent.heartbeat(0.67, 2); console.log("2. Heartbeat sent"); } catch { console.log("2. (offline)"); }
  try { const a = await agent.query("build","spfx"); console.log(`3. Found ${(a as any).agents?.length??0} agent(s)`); } catch { console.log("3. (offline)"); }
  console.log("\n=== Complete ===");
})();
```
