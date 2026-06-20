# Local-First Certification — TypeScript Example

```typescript
/** Local-First Certification v1.0.0 — TypeScript Reference Implementation */
class Client {
  constructor(private api: string = "https://workswithagents.dev") {}
  private async post<T>(path: string, body: Record<string,unknown>): Promise<T> {
    const r = await fetch(`${this.api}${path}`, {method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)});
    if(!r.ok) throw new Error(`Error ${r.status}`);
    return r.json() as Promise<T>;
  }
  async validate_certification(...args: any[]) { return this.post("/v1/local-first/validate-certification", ...args); }
  async check_offline(...args: any[]) { return this.post("/v1/local-first/check-offline", ...args); }
  async audit_external_calls(...args: any[]) { return this.post("/v1/local-first/audit-external-calls", ...args); }
}

(async () => {
  console.log("===Local-First Certification v1.0.0 ===\n");
  const c = new Client();
  const ops = ['validate_certification', 'check_offline', 'audit_external_calls'];
  console.log(`${ops.length} operations: ${ops.join(", ")}`);
  console.log("\n=== Complete ===");
})();
```
