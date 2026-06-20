# Security Disclosure Protocol — TypeScript Example

```typescript
/** Security Disclosure Protocol v1.0.1 — TypeScript Reference Implementation */
class Client {
  constructor(private api: string = "https://workswithagents.dev") {}
  private async post<T>(path: string, body: Record<string,unknown>): Promise<T> {
    const r = await fetch(`${this.api}${path}`, {method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)});
    if(!r.ok) throw new Error(`Error ${r.status}`);
    return r.json() as Promise<T>;
  }
  async submit_finding(...args: any[]) { return this.post("/v1/security-disclosure/submit-finding", ...args); }
  async embargo_finding(...args: any[]) { return this.post("/v1/security-disclosure/embargo-finding", ...args); }
  async notify_vendor(...args: any[]) { return this.post("/v1/security-disclosure/notify-vendor", ...args); }
  async publish_disclosure(...args: any[]) { return this.post("/v1/security-disclosure/publish-disclosure", ...args); }
}

(async () => {
  console.log("===Security Disclosure Protocol v1.0.1 ===\n");
  const c = new Client();
  const ops = ['submit_finding', 'embargo_finding', 'notify_vendor', 'publish_disclosure'];
  console.log(`${ops.length} operations: ${ops.join(", ")}`);
  console.log("\n=== Complete ===");
})();
```
