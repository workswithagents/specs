# Onboarding Protocol — TypeScript Example

Complete TypeScript implementation of the Agent Onboarding Protocol (v1.0.0).

```typescript
/**
 * Onboarding Protocol v1.0.0 — TypeScript Reference Implementation
 *
 * Full flow: INTERVIEW → GENERATE → CALIBRATE → BENCHMARK → REGISTER → DEPLOY
 */

// ── Types ────────────────────────────────────────────────────────

interface InterviewConfig {
  agent_name: string;
  purpose: string;
  capabilities: string[];
  tools: string[];
  skills?: string[];
  trust_tier_target?: string;
  constraints?: string[];
  fleet?: string;
  benchmarks?: {
    task: string;
    target_accuracy: number;
    target_latency_seconds: number;
  }[];
}

interface InterviewResult {
  interview_id: string;
  agent_name: string;
}

interface CalibrationResult {
  passed: boolean;
  results: {
    passed_count: number;
    total_tasks: number;
    tasks: { task_id: string; passed: boolean; score: number }[];
  };
}

interface BenchmarkResult {
  passed: boolean;
  metrics: {
    accuracy: number;
    precision: number;
    recall: number;
    latency_p95: number;
    token_efficiency?: number;
  };
}

interface RegistrationResult {
  agent_id: string;
  trust_score_seed: number;
  tier: string;
}

// ── Client ───────────────────────────────────────────────────────

class OnboardingClient {
  private interviewId: string | null = null;

  constructor(private apiBase: string = "https://workswithagents.dev") {}

  private async post<T>(path: string, body: Record<string, unknown>): Promise<T> {
    const res = await fetch(`${this.apiBase}${path}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: "unknown" }));
      throw new Error(`Onboarding error (${res.status}): ${err.detail}`);
    }
    return res.json() as Promise<T>;
  }

  private async get<T>(path: string): Promise<T> {
    const res = await fetch(`${this.apiBase}${path}`);
    return res.json() as Promise<T>;
  }

  // ── INTERVIEW ──────────────────────────────────────────────

  async startInterview(config: InterviewConfig): Promise<InterviewResult> {
    const body: Record<string, unknown> = {
      agent_name: config.agent_name,
      purpose: config.purpose,
      capabilities: config.capabilities,
      tools: config.tools,
      skills: config.skills ?? [],
      trust_tier_target: config.trust_tier_target ?? "reliable",
      constraints: config.constraints ?? [],
      fleet: config.fleet ?? "auto-detect",
    };
    if (config.benchmarks) body.benchmarks = config.benchmarks;

    const result = await this.post<InterviewResult>("/v1/onboard/interview", body);
    this.interviewId = result.interview_id;
    return result;
  }

  // ── GENERATE ────────────────────────────────────────────────

  async generate(): Promise<{ agent_dir: string }> {
    this.requireInterview();
    return this.post(`/v1/onboard/${this.interviewId}/generate`);
  }

  // ── CALIBRATE ──────────────────────────────────────────────

  async calibrate(): Promise<CalibrationResult> {
    this.requireInterview();
    return this.post(`/v1/onboard/${this.interviewId}/calibrate`);
  }

  // ── BENCHMARK ──────────────────────────────────────────────

  async benchmark(): Promise<BenchmarkResult> {
    this.requireInterview();
    return this.post(`/v1/onboard/${this.interviewId}/benchmark`);
  }

  // ── REGISTER ───────────────────────────────────────────────

  async register(): Promise<RegistrationResult> {
    this.requireInterview();
    return this.post(`/v1/onboard/${this.interviewId}/register`);
  }

  // ── STATUS ─────────────────────────────────────────────────

  async status(): Promise<{ phase: string; completed: boolean }> {
    this.requireInterview();
    return this.get(`/v1/onboard/${this.interviewId}/status`);
  }

  private requireInterview(): asserts this is { interviewId: string } {
    if (!this.interviewId) throw new Error("No interview. Call startInterview() first.");
  }
}

// ── Full Pipeline ─────────────────────────────────────────────────

async function onboardComplianceAgent() {
  const client = new OnboardingClient();
  console.log("=== Onboarding Protocol v1.0.0 ===\n");

  // 1. INTERVIEW
  console.log("1. INTERVIEW — Defining agent: hermes-compliance-checker");
  try {
    const interview = await client.startInterview({
      agent_name: "hermes-compliance-checker",
      purpose: "Validate agent actions against NHS DTAC compliance rules",
      capabilities: ["audit:compliance", "generate:dtac_evidence"],
      tools: ["terminal", "file", "web", "search"],
      skills: ["compliance-as-code", "dtac-validator"],
      constraints: [
        "Never access patient data directly",
        "Always require human sign-off for violation reports",
      ],
      trust_tier_target: "reliable",
      fleet: "regulated-nhs-fleet",
    });
    console.log(`   Interview ID: ${interview.interview_id}`);
  } catch (e) {
    console.log(`   API call (offline): ${(e as Error).message}`);
  }

  // 2. GENERATE
  console.log("\n2. GENERATE — Creating agent artifacts...");
  try {
    const gen = await client.generate();
    console.log(`   Agent dir: ${gen.agent_dir}`);
  } catch (e) {
    console.log(`   API call (offline): ${(e as Error).message}`);
  }

  // 3. CALIBRATE
  console.log("\n3. CALIBRATE — Running calibration...");
  try {
    const cal = await client.calibrate();
    console.log(`   Passed: ${cal.results.passed_count}/${cal.results.total_tasks}`);
    console.log(`   Overall: ${cal.passed ? "✓ PASS" : "✗ FAIL"}`);
  } catch (e) {
    console.log(`   API call (offline): ${(e as Error).message}`);
  }

  // 4. BENCHMARK
  console.log("\n4. BENCHMARK — Full test suite...");
  try {
    const bench = await client.benchmark();
    console.log(`   Accuracy:    ${bench.metrics.accuracy}`);
    console.log(`   Precision:   ${bench.metrics.precision}`);
    console.log(`   Recall:      ${bench.metrics.recall}`);
    console.log(`   P95 Latency: ${bench.metrics.latency_p95}s`);
    console.log(`   Overall:     ${bench.passed ? "✓ PASS" : "✗ FAIL"}`);
  } catch (e) {
    console.log(`   API call (offline): ${(e as Error).message}`);
  }

  // 5. REGISTER
  console.log("\n5. REGISTER — Publishing to registry...");
  try {
    const reg = await client.register();
    console.log(`   Agent ID:  ${reg.agent_id}`);
    console.log(`   Trust:     ${reg.trust_score_seed}`);
    console.log(`   Tier:      ${reg.tier}`);
  } catch (e) {
    console.log(`   API call (offline): ${(e as Error).message}`);
  }

  console.log("\n6. DEPLOY — Agent joins fleet: regulated-nhs-fleet");
  console.log("\n=== Onboarding Complete ===");
}

onboardComplianceAgent().catch(console.error);
```
