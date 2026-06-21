# Deployment Manifest — TypeScript Example

```typescript
/** Deployment Manifest v1.0.0 — TypeScript Reference Implementation */
class Client {
  constructor(private api: string = "https://workswithagents.dev") {}
  private async post<T>(path: string, body: Record<string,unknown>): Promise<T> {
    const r = await fetch(`${this.api}${path}`, {method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)});
    if(!r.ok) throw new Error(`Error ${r.status}`);
    return r.json() as Promise<T>;
  }
  async deploy_fleet(...args: any[]) { return this.post("/v1/deployment/deploy-fleet", ...args); }
  async validate_manifest(...args: any[]) { return this.post("/v1/deployment/validate-manifest", ...args); }
  async scale_agents(...args: any[]) { return this.post("/v1/deployment/scale-agents", ...args); }
  async get_status(...args: any[]) { return this.post("/v1/deployment/get-status", ...args); }
}

(async () => {
  console.log("===Deployment Manifest v1.0.0 ===\n");
  const c = new Client();
  const ops = ['deploy_fleet', 'validate_manifest', 'scale_agents', 'get_status'];
  console.log(`${ops.length} operations: ${ops.join(", ")}`);
  console.log("\n=== Complete ===");
})();
```
