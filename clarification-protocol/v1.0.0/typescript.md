# Clarification Protocol — TypeScript Example

```typescript
/** Clarification Protocol v1.0.0 — TypeScript Reference Implementation */
class Client {
  constructor(private api: string = "https://workswithagents.dev") {}
  private async post<T>(path: string, body: Record<string,unknown>): Promise<T> {
    const r = await fetch(`${this.api}${path}`, {method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)});
    if(!r.ok) throw new Error(`Error ${r.status}`);
    return r.json() as Promise<T>;
  }
  async submit_clarification(...args: any[]) { return this.post("/v1/clarification/submit-clarification", ...args); }
  async resolve_gap(...args: any[]) { return this.post("/v1/clarification/resolve-gap", ...args); }
  async list_gaps(...args: any[]) { return this.post("/v1/clarification/list-gaps", ...args); }
  async session_status(...args: any[]) { return this.post("/v1/clarification/session-status", ...args); }
}

(async () => {
  console.log("===Clarification Protocol v1.0.0 ===\n");
  const c = new Client();
  const ops = ['submit_clarification', 'resolve_gap', 'list_gaps', 'session_status'];
  console.log(`${ops.length} operations: ${ops.join(", ")}`);
  console.log("\n=== Complete ===");
})();
```
