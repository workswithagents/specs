# Delegation Framework — TypeScript Example

```typescript
/** Delegation Framework v1.0.0 — TypeScript Reference Implementation */
class Client {
  constructor(private api: string = "https://workswithagents.dev") {}
  private async post<T>(path: string, body: Record<string,unknown>): Promise<T> {
    const r = await fetch(`${this.api}${path}`, {method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)});
    if(!r.ok) throw new Error(`Error ${r.status}`);
    return r.json() as Promise<T>;
  }
  async issue_delegation(...args: any[]) { return this.post("/v1/delegation/issue-delegation", ...args); }
  async verify_delegation(...args: any[]) { return this.post("/v1/delegation/verify-delegation", ...args); }
  async revoke_delegation(...args: any[]) { return this.post("/v1/delegation/revoke-delegation", ...args); }
  async list_delegations(...args: any[]) { return this.post("/v1/delegation/list-delegations", ...args); }
}

(async () => {
  console.log("===Delegation Framework v1.0.0 ===\n");
  const c = new Client();
  const ops = ['issue_delegation', 'verify_delegation', 'revoke_delegation', 'list_delegations'];
  console.log(`${ops.length} operations: ${ops.join(", ")}`);
  console.log("\n=== Complete ===");
})();
```
