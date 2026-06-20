# Agent Economics Protocol — TypeScript Example

```typescript
/** Agent Economics Protocol v1.0.0 — TypeScript Reference Implementation */
class Client {
  constructor(private api: string = "https://workswithagents.dev") {}
  private async post<T>(path: string, body: Record<string,unknown>): Promise<T> {
    const r = await fetch(`${this.api}${path}`, {method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)});
    if(!r.ok) throw new Error(`Error ${r.status}`);
    return r.json() as Promise<T>;
  }
  async transfer_credits(...args: any[]) { return this.post("/v1/economics/transfer-credits", ...args); }
  async create_bounty(...args: any[]) { return this.post("/v1/economics/create-bounty", ...args); }
  async settle_task(...args: any[]) { return this.post("/v1/economics/settle-task", ...args); }
  async get_balance(...args: any[]) { return this.post("/v1/economics/get-balance", ...args); }
}

(async () => {
  console.log("===Agent Economics Protocol v1.0.0 ===\n");
  const c = new Client();
  const ops = ['transfer_credits', 'create_bounty', 'settle_task', 'get_balance'];
  console.log(`${ops.length} operations: ${ops.join(", ")}`);
  console.log("\n=== Complete ===");
})();
```
