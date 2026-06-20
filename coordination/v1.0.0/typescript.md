# Coordination Protocol (ACP) — TypeScript Example

```typescript
/** Coordination Protocol (ACP) v1.0.0 — TypeScript Reference Implementation */
class Client {
  constructor(private api: string = "https://workswithagents.dev") {}
  private async post<T>(path: string, body: Record<string,unknown>): Promise<T> {
    const r = await fetch(`${this.api}${path}`, {method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)});
    if(!r.ok) throw new Error(`Error ${r.status}`);
    return r.json() as Promise<T>;
  }
  async elect_leader(...args: any[]) { return this.post("/v1/coordination/elect-leader", ...args); }
  async distribute_work(...args: any[]) { return this.post("/v1/coordination/distribute-work", ...args); }
  async steal_work(...args: any[]) { return this.post("/v1/coordination/steal-work", ...args); }
  async heartbeat(...args: any[]) { return this.post("/v1/coordination/heartbeat", ...args); }
}

(async () => {
  console.log("===Coordination Protocol (ACP) v1.0.0 ===\n");
  const c = new Client();
  const ops = ['elect_leader', 'distribute_work', 'steal_work', 'heartbeat'];
  console.log(`${ops.length} operations: ${ops.join(", ")}`);
  console.log("\n=== Complete ===");
})();
```
