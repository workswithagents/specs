# Reputation Ledger — TypeScript Example

```typescript
/** Reputation Ledger v1.0.0 — TypeScript Reference Implementation */
class Client {
  constructor(private api: string = "https://workswithagents.dev") {}
  private async post<T>(path: string, body: Record<string,unknown>): Promise<T> {
    const r = await fetch(`${this.api}${path}`, {method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)});
    if(!r.ok) throw new Error(`Error ${r.status}`);
    return r.json() as Promise<T>;
  }
  async record_claim(...args: any[]) { return this.post("/v1/reputation/record-claim", ...args); }
  async verify_claim(...args: any[]) { return this.post("/v1/reputation/verify-claim", ...args); }
  async get_reputation(...args: any[]) { return this.post("/v1/reputation/get-reputation", ...args); }
  async challenge_claim(...args: any[]) { return this.post("/v1/reputation/challenge-claim", ...args); }
}

(async () => {
  console.log("===Reputation Ledger v1.0.0 ===\n");
  const c = new Client();
  const ops = ['record_claim', 'verify_claim', 'get_reputation', 'challenge_claim'];
  console.log(`${ops.length} operations: ${ops.join(", ")}`);
  console.log("\n=== Complete ===");
})();
```
