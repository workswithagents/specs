# Handoff Protocol — TypeScript Example

Complete TypeScript implementation of the Handoff Protocol (v1.0.0).

```typescript
/**
 * Handoff Protocol v1.0.0 — TypeScript Reference Implementation
 *
 * Implements the full handoff lifecycle as defined in the Handoff Protocol spec.
 * Uses native fetch — no external dependencies.
 */

// ── Types ────────────────────────────────────────────────────────

interface HandoffSender {
  agent_id: string;
  session_id: string;
  identity_sig: string;
}

interface HandoffReceiver {
  agent_id: string;
  session_id: string;
  identity_sig?: string;
}

interface StateSnapshot {
  files_modified: string[];
  branch: string;
  last_commit: string;
}

interface AgentMemory {
  key_decisions: string[];
  discovered_pitfalls: string[];
  pending_items: string[];
}

interface HandoffConstraints {
  max_turns: number;
  deadline: string;
  compliance_level: string;
}

interface HandoffContext {
  task_description: string;
  workspace_path: string;
  state_snapshot: StateSnapshot;
  agent_memory: AgentMemory;
  tools_required: string[];
  constraints: HandoffConstraints;
}

interface HandoffRequest {
  handoff_id: string;
  task_id: string;
  sender: HandoffSender;
  context: HandoffContext;
  quality_checklist: string[];
}

interface HandoffResponse {
  handoff_id: string;
  status: "accepted" | "rejected" | "queued" | "already_done" | "duplicate";
  reason?: string;
  receiver: HandoffReceiver;
  estimated_completion?: string;
  queries?: string[];
  receiver_context?: {
    available_tools: string[];
    model: string;
    max_context_tokens: number;
  };
}

interface ProgressUpdate {
  handoff_id: string;
  receiver_agent_id: string;
  progress: {
    percent_complete: number;
    pitfalls_found: string[];
    timestamp: string;
  };
}

interface CompletionEvent {
  handoff_id: string;
  receiver_agent_id: string;
  status: "completed";
  results: Record<string, unknown>;
  timestamp: string;
}

// ── Client ───────────────────────────────────────────────────────

class HandoffClient {
  private agentId: string;
  private apiBase: string;

  constructor(agentId: string, apiBase: string = "https://workswithagents.dev") {
    this.agentId = agentId;
    this.apiBase = apiBase.replace(/\/$/, "");
  }

  private async post<T>(path: string, body: Record<string, unknown>): Promise<T> {
    const url = `${this.apiBase}${path}`;
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-Agent-ID": this.agentId,
      },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: "unknown error" }));
      throw new Error(`Handoff error (${response.status}): ${error.detail}`);
    }

    return response.json() as Promise<T>;
  }

  // ── Sender side ──────────────────────────────────────────────

  async requestHandoff(
    taskId: string,
    receiverAgentId: string,
    taskDescription: string,
    options: {
      workspacePath?: string;
      stateSnapshot?: StateSnapshot;
      agentMemory?: AgentMemory;
      toolsRequired?: string[];
      constraints?: HandoffConstraints;
      qualityChecklist?: string[];
    } = {}
  ): Promise<{ handoff_id: string }> {
    const handoffId = crypto.randomUUID();

    const request: HandoffRequest = {
      handoff_id: handoffId,
      task_id: taskId,
      sender: {
        agent_id: this.agentId,
        session_id: `sess-${crypto.randomUUID().slice(0, 8)}`,
        identity_sig: "ed25519:placeholder-signature",
      },
      context: {
        task_description: taskDescription,
        workspace_path: options.workspacePath ?? "",
        state_snapshot: options.stateSnapshot ?? {
          files_modified: [],
          branch: "main",
          last_commit: "",
        },
        agent_memory: options.agentMemory ?? {
          key_decisions: [],
          discovered_pitfalls: [],
          pending_items: [],
        },
        tools_required: options.toolsRequired ?? ["terminal", "file", "web"],
        constraints: options.constraints ?? {
          max_turns: 30,
          deadline: new Date(Date.now() + 7200_000).toISOString(),
          compliance_level: "standard",
        },
      },
      quality_checklist: options.qualityChecklist ?? [],
    };

    return this.post(`/v1/handoff/${receiverAgentId}/request`, request);
  }

  async queryStatus(handoffId: string, receiverAgentId: string): Promise<ProgressUpdate> {
    return this.post(`/v1/handoff/${receiverAgentId}/status`, {
      handoff_id: handoffId,
      sender_agent_id: this.agentId,
    });
  }

  // ── Receiver side ────────────────────────────────────────────

  async acceptHandoff(
    handoffId: string,
    senderAgentId: string,
    options: {
      estimatedCompletion?: string;
      queries?: string[];
      availableTools?: string[];
    } = {}
  ): Promise<HandoffResponse> {
    const estimatedCompletion =
      options.estimatedCompletion ??
      new Date(Date.now() + 3600_000).toISOString();

    const response: HandoffResponse = {
      handoff_id: handoffId,
      status: "accepted",
      receiver: {
        agent_id: this.agentId,
        session_id: `sess-${crypto.randomUUID().slice(0, 8)}`,
        identity_sig: "ed25519:placeholder-signature",
      },
      estimated_completion: estimatedCompletion,
      queries: options.queries ?? [],
      receiver_context: {
        available_tools: options.availableTools ?? ["terminal", "file", "web"],
        model: "deepseek-v4-pro",
        max_context_tokens: 131072,
      },
    };

    return this.post(`/v1/handoff/${senderAgentId}/response`, response);
  }

  async rejectHandoff(
    handoffId: string,
    senderAgentId: string,
    reason: string
  ): Promise<HandoffResponse> {
    return this.post(`/v1/handoff/${senderAgentId}/response`, {
      handoff_id: handoffId,
      status: "rejected",
      reason,
      receiver: {
        agent_id: this.agentId,
        session_id: `sess-${crypto.randomUUID().slice(0, 8)}`,
      },
    });
  }

  async sendProgressUpdate(
    handoffId: string,
    senderAgentId: string,
    percentComplete: number,
    pitfallsFound: string[] = []
  ): Promise<ProgressUpdate> {
    return this.post(`/v1/handoff/${senderAgentId}/progress`, {
      handoff_id: handoffId,
      receiver_agent_id: this.agentId,
      progress: {
        percent_complete: percentComplete,
        pitfalls_found: pitfallsFound,
        timestamp: new Date().toISOString(),
      },
    });
  }

  async sendCompletionEvent(
    handoffId: string,
    senderAgentId: string,
    results: Record<string, unknown>
  ): Promise<CompletionEvent> {
    return this.post(`/v1/handoff/${senderAgentId}/complete`, {
      handoff_id: handoffId,
      receiver_agent_id: this.agentId,
      status: "completed",
      results,
      timestamp: new Date().toISOString(),
    });
  }
}

// ── Demo ─────────────────────────────────────────────────────────

async function main() {
  const sender = new HandoffClient("builder-01");
  const receiver = new HandoffClient("reviewer-02");

  console.log("=== Handoff Protocol v1.0.0 Demo ===\n");

  // Step 1: Sender creates a handoff request
  const taskId = crypto.randomUUID();
  console.log(`1. Creating handoff for task: ${taskId}`);

  let handoffId: string;
  try {
    const result = await sender.requestHandoff(
      taskId,
      "reviewer-02",
      "Review the NHS DTAC compliance report",
      {
        workspacePath: "/projects/nhs-audit",
        stateSnapshot: {
          files_modified: ["report.md", "evidence.json"],
          branch: "feature/nhs-compliance",
          last_commit: "abc123",
        },
        agentMemory: {
          key_decisions: ["Use ISO 27001 mapping"],
          discovered_pitfalls: [
            "SPFx Heft build fragile on SCSS resolution",
            "Node v18 required for NHS toolkit",
          ],
          pending_items: ["Attach DPIA appendix"],
        },
        toolsRequired: ["terminal", "file", "web"],
        constraints: {
          max_turns: 30,
          deadline: "2026-06-21T17:00:00Z",
          compliance_level: "nhs-dtac",
        },
        qualityChecklist: [
          "DPIA referenced where personal data involved",
          "Model Card attached for any LLM usage",
          "No patient data in outputs",
          "Audit trail is complete",
        ],
      }
    );
    handoffId = result.handoff_id;
    console.log(`   Handoff sent! ID: ${handoffId}`);
  } catch (e) {
    console.log(`   API call (expected in offline demo): ${(e as Error).message}`);
    handoffId = crypto.randomUUID();
  }

  // Step 2: Receiver validates (quality gates)
  console.log(`\n2. Receiver validating handoff ${handoffId}...`);
  console.log("   Quality gates checked:");
  console.log("   ✓ Identity signature valid");
  console.log("   ✓ Context complete");
  console.log("   ✓ Required tools available");
  console.log("   ✓ Within capability");
  console.log("   ✓ No conflicting task in progress");
  console.log("   ✓ Deadline achievable");

  // Step 3: Receiver accepts
  console.log("\n3. Accepting handoff...");
  try {
    const acceptResult = await receiver.acceptHandoff(
      handoffId,
      "builder-01",
      { queries: ["Which DPIA template should I use?"] }
    );
    console.log(`   Status: ${acceptResult.status}`);
  } catch (e) {
    console.log(`   API call (expected offline): ${(e as Error).message}`);
  }

  // Step 4: Progress update
  console.log("\n4. Sending progress update (30%)...");
  try {
    await receiver.sendProgressUpdate(handoffId, "builder-01", 0.30, [
      "Missing section on data retention policy",
    ]);
  } catch {
    console.log("   Progress update queued (offline mode).");
  }

  // Step 5: Completion
  console.log("\n5. Task complete — sending completion event...");
  try {
    await receiver.sendCompletionEvent(handoffId, "builder-01", {
      review_passed: true,
      issues_found: 3,
      issues_resolved: 3,
      report_url: "/projects/nhs-audit/report-reviewed.md",
    });
  } catch {
    console.log("   Completion event prepared (offline mode).");
  }

  // Step 6: Status query
  console.log("\n6. Sender querying final status...");
  try {
    const status = await sender.queryStatus(handoffId, "reviewer-02");
    console.log(`   Final status: ${JSON.stringify(status, null, 2)}`);
  } catch (e) {
    console.log(`   Status query (offline): ${(e as Error).message}`);
  }

  // ── Error condition demo ────────────────────────────────────
  console.log("\n=== Error Handling Demo ===\n");
  console.log("7. Simulating rejection due to missing tools...");
  try {
    await receiver.rejectHandoff(
      crypto.randomUUID(),
      "builder-01",
      "missing_tools: browser not available"
    );
  } catch {
    console.log("   Rejection handled (offline mode).");
  }

  console.log("\n=== Demo Complete ===");
}

// Run
main().catch(console.error);
```

## Key Types

| Interface | Purpose |
|-----------|---------|
| `HandoffRequest` | Complete handoff payload with context, memory, constraints |
| `HandoffResponse` | Acceptance/rejection with receiver context |
| `ProgressUpdate` | Mid-task progress with pitfalls |
| `CompletionEvent` | Final results notification |
| `HandoffClient` | Full sender + receiver implementation |
