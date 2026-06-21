# Ephemeral Communication Protocol — TypeScript Example

```typescript
/** Ephemeral Communication Protocol v1.0.0 — TypeScript Reference Implementation */
class Client {
  constructor(private api: string = "https://workswithagents.dev") {}
  private async post<T>(path: string, body: Record<string,unknown>): Promise<T> {
    const r = await fetch(`${this.api}${path}`, {method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)});
    if(!r.ok) throw new Error(`Error ${r.status}`);
    return r.json() as Promise<T>;
  }
  async create_room(...args: any[]) { return this.post("/v1/ecp/create-room", ...args); }
  async send_message(...args: any[]) { return this.post("/v1/ecp/send-message", ...args); }
  async destroy_room(...args: any[]) { return this.post("/v1/ecp/destroy-room", ...args); }
  async get_ttl(...args: any[]) { return this.post("/v1/ecp/get-ttl", ...args); }
}

(async () => {
  console.log("===Ephemeral Communication Protocol v1.0.0 ===\n");
  const c = new Client();
  const ops = ['create_room', 'send_message', 'destroy_room', 'get_ttl'];
  console.log(`${ops.length} operations: ${ops.join(", ")}`);
  console.log("\n=== Complete ===");
})();
```
