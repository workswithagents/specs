# Agent Coding Benchmark — TypeScript Example

```typescript
/** Agent Coding Benchmark v1.0.0 — TypeScript Reference Implementation */
class Client {
  constructor(private api: string = "https://workswithagents.dev") {}
  private async post<T>(path: string, body: Record<string,unknown>): Promise<T> {
    const r = await fetch(`${this.api}${path}`, {method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)});
    if(!r.ok) throw new Error(`Error ${r.status}`);
    return r.json() as Promise<T>;
  }
  async run_benchmark(...args: any[]) { return this.post("/v1/benchmark/run-benchmark", ...args); }
  async get_results(...args: any[]) { return this.post("/v1/benchmark/get-results", ...args); }
  async compare_models(...args: any[]) { return this.post("/v1/benchmark/compare-models", ...args); }
}

(async () => {
  console.log("===Agent Coding Benchmark v1.0.0 ===\n");
  const c = new Client();
  const ops = ['run_benchmark', 'get_results', 'compare_models'];
  console.log(`${ops.length} operations: ${ops.join(", ")}`);
  console.log("\n=== Complete ===");
})();
```
