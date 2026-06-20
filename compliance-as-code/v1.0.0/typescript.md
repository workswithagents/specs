# Compliance-as-Code — TypeScript Example

```typescript
/** Compliance-as-Code v1.0.0 — TypeScript Reference Implementation */
class Client {
  constructor(private api: string = "https://workswithagents.dev") {}
  private async post<T>(path: string, body: Record<string,unknown>): Promise<T> {
    const r = await fetch(`${this.api}${path}`, {method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)});
    if(!r.ok) throw new Error(`Error ${r.status}`);
    return r.json() as Promise<T>;
  }
  async validate_rules(...args: any[]) { return this.post("/v1/compliance/validate-rules", ...args); }
  async check_compliance(...args: any[]) { return this.post("/v1/compliance/check-compliance", ...args); }
  async run_audit(...args: any[]) { return this.post("/v1/compliance/run-audit", ...args); }
  async generate_report(...args: any[]) { return this.post("/v1/compliance/generate-report", ...args); }
}

(async () => {
  console.log("===Compliance-as-Code v1.0.0 ===\n");
  const c = new Client();
  const ops = ['validate_rules', 'check_compliance', 'run_audit', 'generate_report'];
  console.log(`${ops.length} operations: ${ops.join(", ")}`);
  console.log("\n=== Complete ===");
})();
```
