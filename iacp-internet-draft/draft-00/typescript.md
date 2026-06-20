# IACP Internet Draft — TypeScript Example

```typescript
/** IACP Internet Draft vdraft-00 — TypeScript Reference Implementation */
class Client {
  constructor(private api: string = "https://workswithagents.dev") {}
  private async post<T>(path: string, body: Record<string,unknown>): Promise<T> {
    const r = await fetch(`${this.api}${path}`, {method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)});
    if(!r.ok) throw new Error(`Error ${r.status}`);
    return r.json() as Promise<T>;
  }
  async discover_peers(...args: any[]) { return this.post("/v1/iacp/discover-peers", ...args); }
  async send_message(...args: any[]) { return this.post("/v1/iacp/send-message", ...args); }
  async poll_inbox(...args: any[]) { return this.post("/v1/iacp/poll-inbox", ...args); }
  async heartbeat(...args: any[]) { return this.post("/v1/iacp/heartbeat", ...args); }
}

(async () => {
  console.log("===IACP Internet Draft vdraft-00 ===\n");
  const c = new Client();
  const ops = ['discover_peers', 'send_message', 'poll_inbox', 'heartbeat'];
  console.log(`${ops.length} operations: ${ops.join(", ")}`);
  console.log("\n=== Complete ===");
})();
```
