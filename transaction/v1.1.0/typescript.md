# Transaction Protocol (ATP) — TypeScript Example

```typescript
/** Transaction Protocol (ATP) v1.0.0 — TypeScript Reference Implementation */
class Client {
  constructor(private api: string = "https://workswithagents.dev") {}
  private async post<T>(path: string, body: Record<string,unknown>): Promise<T> {
    const r = await fetch(`${this.api}${path}`, {method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)});
    if(!r.ok) throw new Error(`Error ${r.status}`);
    return r.json() as Promise<T>;
  }
  async create_transaction(...args: any[]) { return this.post("/v1/transaction/create-transaction", ...args); }
  async commit(...args: any[]) { return this.post("/v1/transaction/commit", ...args); }
  async rollback(...args: any[]) { return this.post("/v1/transaction/rollback", ...args); }
  async get_status(...args: any[]) { return this.post("/v1/transaction/get-status", ...args); }
}

(async () => {
  console.log("===Transaction Protocol (ATP) v1.0.0 ===\n");
  const c = new Client();
  const ops = ['create_transaction', 'commit', 'rollback', 'get_status'];
  console.log(`${ops.length} operations: ${ops.join(", ")}`);
  console.log("\n=== Complete ===");
})();
```
