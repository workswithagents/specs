# AI Gateway / Policy Enforcement Point — TypeScript Example

```typescript
/** AI Gateway / Policy Enforcement Point v1.0.0 — TypeScript Reference Implementation */
class Client {
  constructor(private api: string = "https://workswithagents.dev") {}
  private async post<T>(path: string, body: Record<string,unknown>): Promise<T> {
    const r = await fetch(`${this.api}${path}`, {method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)});
    if(!r.ok) throw new Error(`Error ${r.status}`);
    return r.json() as Promise<T>;
  }
  async enforce_policy(...args: any[]) { return this.post("/v1/gateway/enforce-policy", ...args); }
  async check_rate_limit(...args: any[]) { return this.post("/v1/gateway/check-rate-limit", ...args); }
  async audit_request(...args: any[]) { return this.post("/v1/gateway/audit-request", ...args); }
  async block_request(...args: any[]) { return this.post("/v1/gateway/block-request", ...args); }
}

(async () => {
  console.log("===AI Gateway / Policy Enforcement Point v1.0.0 ===\n");
  const c = new Client();
  const ops = ['enforce_policy', 'check_rate_limit', 'audit_request', 'block_request'];
  console.log(`${ops.length} operations: ${ops.join(", ")}`);
  console.log("\n=== Complete ===");
})();
```
