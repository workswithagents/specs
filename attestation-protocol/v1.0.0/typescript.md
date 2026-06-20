# Attestation Protocol — TypeScript Example

```typescript
/** Attestation Protocol v1.0.0 — TypeScript Reference Implementation */
class Client {
  constructor(private api: string = "https://workswithagents.dev") {}
  private async post<T>(path: string, body: Record<string,unknown>): Promise<T> {
    const r = await fetch(`${this.api}${path}`, {method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)});
    if(!r.ok) throw new Error(`Error ${r.status}`);
    return r.json() as Promise<T>;
  }
  async generate_attestation(...args: any[]) { return this.post("/v1/attestation/generate-attestation", ...args); }
  async verify_attestation(...args: any[]) { return this.post("/v1/attestation/verify-attestation", ...args); }
  async get_chain(...args: any[]) { return this.post("/v1/attestation/get-chain", ...args); }
}

(async () => {
  console.log("===Attestation Protocol v1.0.0 ===\n");
  const c = new Client();
  const ops = ['generate_attestation', 'verify_attestation', 'get_chain'];
  console.log(`${ops.length} operations: ${ops.join(", ")}`);
  console.log("\n=== Complete ===");
})();
```
