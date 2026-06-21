# AP2 Payment Mandate — TypeScript Example

```typescript
/** AP2 Payment Mandate v0.9.0 — TypeScript Reference Implementation */
class Client {
  constructor(private api: string = "https://workswithagents.dev") {}
  private async post<T>(path: string, body: Record<string,unknown>): Promise<T> {
    const r = await fetch(`${this.api}${path}`, {method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)});
    if(!r.ok) throw new Error(`Error ${r.status}`);
    return r.json() as Promise<T>;
  }
  async create_mandate(...args: any[]) { return this.post("/v1/ap2/create-mandate", ...args); }
  async verify_spend(...args: any[]) { return this.post("/v1/ap2/verify-spend", ...args); }
  async revoke_mandate(...args: any[]) { return this.post("/v1/ap2/revoke-mandate", ...args); }
  async get_spend_history(...args: any[]) { return this.post("/v1/ap2/get-spend-history", ...args); }
}

(async () => {
  console.log("===AP2 Payment Mandate v0.9.0 ===\n");
  const c = new Client();
  const ops = ['create_mandate', 'verify_spend', 'revoke_mandate', 'get_spend_history'];
  console.log(`${ops.length} operations: ${ops.join(", ")}`);
  console.log("\n=== Complete ===");
})();
```
