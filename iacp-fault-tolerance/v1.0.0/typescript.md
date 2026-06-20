# IACP Fault Tolerance — TypeScript Example

```typescript
/** IACP Fault Tolerance v1.0.0 — TypeScript Reference Implementation */
class Client {
  constructor(private api: string = "https://workswithagents.dev") {}
  private async post<T>(path: string, body: Record<string,unknown>): Promise<T> {
    const r = await fetch(`${this.api}${path}`, {method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)});
    if(!r.ok) throw new Error(`Error ${r.status}`);
    return r.json() as Promise<T>;
  }
  async detect_timeout(...args: any[]) { return this.post("/v1/iacp/fault-tolerance/detect-timeout", ...args); }
  async handle_dead_letter(...args: any[]) { return this.post("/v1/iacp/fault-tolerance/handle-dead-letter", ...args); }
  async rollback(...args: any[]) { return this.post("/v1/iacp/fault-tolerance/rollback", ...args); }
  async retry_with_backoff(...args: any[]) { return this.post("/v1/iacp/fault-tolerance/retry-with-backoff", ...args); }
}

(async () => {
  console.log("===IACP Fault Tolerance v1.0.0 ===\n");
  const c = new Client();
  const ops = ['detect_timeout', 'handle_dead_letter', 'rollback', 'retry_with_backoff'];
  console.log(`${ops.length} operations: ${ops.join(", ")}`);
  console.log("\n=== Complete ===");
})();
```
