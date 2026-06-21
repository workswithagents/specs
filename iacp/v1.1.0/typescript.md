# IACP — TypeScript Example

Complete TypeScript implementation of IACP — Inter-Agent Communication Protocol (v1.0.0).

```typescript
/**
 * IACP v1.0.0 — TypeScript Reference Implementation
 *
 * Full IACP client: Peer Discovery, Messaging, Capability Queries, Negotiation.
 * Uses native fetch — no external dependencies.
 */

// ── Types ────────────────────────────────────────────────────────

type MessageType = "request" | "response" | "event" | "error" | "heartbeat";
type MessageIntent = "handoff" | "query" | "negotiate" | "notify" | "health";

interface EnvelopeSender {
  agent_id: string;
  identity_sig?: string;
}

interface EnvelopeRecipient {
  agent_id: string;
  channel?: string;
}

interface IACPMessage {
  type: MessageType;
  intent: MessageIntent;
  payload: Record<string, unknown>;
}

interface IACPEnvelope {
  version: "1.0";
  message_id: string;
  correlation_id?: string;
  sender: EnvelopeSender;
  recipient: EnvelopeRecipient;
  timestamp: string;
  ttl_seconds?: number;
  message: IACPMessage;
}

interface Peer {
  agent_id: string;
  capabilities: string[];
  availability?: "idle" | "busy" | "offline";
  load?: number;
}

// ── Client ───────────────────────────────────────────────────────

class IACPClient {
  private agentId: string;
  private apiBase: string;

  private static readonly VALID_INTENTS = new Set<MessageIntent>([
    "handoff", "query", "negotiate", "notify", "health",
  ]);
  private static readonly VALID_TYPES = new Set<MessageType>([
    "request", "response", "event", "error", "heartbeat",
  ]);

  constructor(agentId: string, apiBase: string = "https://workswithagents.dev") {
    this.agentId = agentId;
    this.apiBase = apiBase.replace(/\/$/, "");
  }

  private async request<T>(method: string, path: string, body?: Record<string, unknown>): Promise<T> {
    const url = `${this.apiBase}${path}`;
    const options: RequestInit = {
      method,
      headers: {
        "Content-Type": "application/json",
        "X-Agent-ID": this.agentId,
      },
    };
    if (body) options.body = JSON.stringify(body);
    const res = await fetch(url, options);
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: "unknown" }));
      throw new Error(`IACP error (${res.status}): ${err.detail}`);
    }
    return res.json() as Promise<T>;
  }

  // ── Peer Discovery ──────────────────────────────────────────

  async discover(capability?: string): Promise<Peer[]> {
    let path = "/v1/peers";
    if (capability) path += `?capability=${encodeURIComponent(capability)}`;
    return this.request("GET", path);
  }

  async broadcastPresence(capabilities: string[]): Promise<void> {
    await this.request("POST", "/v1/peers/announce", {
      agent_id: this.agentId,
      capabilities,
      timestamp: new Date().toISOString(),
    });
  }

  // ── Send Message ────────────────────────────────────────────

  async send(
    toAgent: string,
    intent: MessageIntent,
    payload: Record<string, unknown>,
    options?: {
      msgType?: MessageType;
      correlationId?: string;
      ttlSeconds?: number;
    }
  ): Promise<string> {
    if (!IACPClient.VALID_INTENTS.has(intent)) {
      throw new Error(`Invalid intent '${intent}'`);
    }
    const msgType = options?.msgType ?? "request";
    if (!IACPClient.VALID_TYPES.has(msgType)) {
      throw new Error(`Invalid type '${msgType}'`);
    }

    const envelope: IACPEnvelope = {
      version: "1.0",
      message_id: crypto.randomUUID(),
      correlation_id: options?.correlationId ?? crypto.randomUUID(),
      sender: {
        agent_id: this.agentId,
        identity_sig: "ed25519:placeholder-signature",
      },
      recipient: {
        agent_id: toAgent,
        channel: intent,
      },
      timestamp: new Date().toISOString(),
      ttl_seconds: options?.ttlSeconds ?? 3600,
      message: {
        type: msgType,
        intent,
        payload,
      },
    };

    const result = await this.request<{ message_id: string }>("POST", "/v1/messages", envelope);
    return result.message_id ?? envelope.message_id;
  }

  // ── Poll Inbox ─────────────────────────────────────────────

  async poll(since?: string, limit: number = 50): Promise<IACPEnvelope[]> {
    let path = `/v1/messages?recipient=${this.agentId}&limit=${limit}`;
    if (since) path += `&since=${encodeURIComponent(since)}`;
    return this.request("GET", path);
  }

  // ── Capability Query ────────────────────────────────────────

  async queryCapability(
    toAgent: string,
    capabilities: string[] = ["code_review", "testing"],
    maxTokens: number = 4096,
    priority: string = "normal"
  ): Promise<IACPEnvelope> {
    return this.request("POST", "/v1/messages", {
      version: "1.0",
      message_id: crypto.randomUUID(),
      sender: { agent_id: this.agentId },
      recipient: { agent_id: toAgent },
      timestamp: new Date().toISOString(),
      message: {
        type: "request",
        intent: "query",
        payload: { capabilities, max_tokens: maxTokens, priority },
      },
    });
  }

  // ── Negotiation ─────────────────────────────────────────────

  async negotiate(
    toAgent: string,
    task: string,
    rewardCredits: number,
    deadline: string
  ): Promise<void> {
    await this.send(toAgent, "negotiate", {
      task,
      reward_credits: rewardCredits,
      deadline,
    });
  }

  async respondNegotiate(
    toAgent: string,
    correlationId: string,
    accept: boolean,
    counterOffer?: Record<string, unknown>
  ): Promise<void> {
    const payload: Record<string, unknown> = { accept };
    if (counterOffer) payload.counter = counterOffer;

    await this.send(toAgent, "negotiate", payload, {
      msgType: "response",
      correlationId,
    });
  }

  // ── Heartbeat ───────────────────────────────────────────────

  async heartbeat(status: string = "healthy", load: number = 0.0): Promise<void> {
    await this.request("POST", "/v1/heartbeat", {
      agent_id: this.agentId,
      status,
      load,
      timestamp: new Date().toISOString(),
    });
  }
}

// ── Demo ─────────────────────────────────────────────────────────

async function main() {
  console.log("=== IACP v1.0.0 Demo ===\n");

  const builder = new IACPClient("builder-01");
  const reviewer = new IACPClient("reviewer-02");

  // 1. Peer Discovery
  console.log("1. Discovering peers...");
  try {
    const peers = await builder.discover("code_review");
    console.log(`   Found ${peers.length} peer(s)`);
    for (const p of peers.slice(0, 3)) {
      console.log(`   - ${p.agent_id}: ${p.capabilities.join(", ")}`);
    }
  } catch (e) {
    console.log(`   API call (offline): ${(e as Error).message}`);
  }

  // 2. Broadcast Presence
  console.log("\n2. Broadcasting presence...");
  try {
    await builder.broadcastPresence(["code_gen", "testing"]);
    await reviewer.broadcastPresence(["code_review", "security_audit"]);
    console.log("   Both agents announced.");
  } catch (e) {
    console.log(`   API call (offline): ${(e as Error).message}`);
  }

  // 3. Send query
  console.log("\n3. Sending capability query...");
  try {
    const msgId = await builder.send("reviewer-02", "query", {
      capabilities: ["code_review", "testing"],
      max_tokens: 4096,
      priority: "high",
    });
    console.log(`   Message sent! ID: ${msgId}`);
  } catch (e) {
    console.log(`   API call (offline): ${(e as Error).message}`);
  }

  // 4. Handoff over IACP
  console.log("\n4. Sending handoff via IACP envelope...");
  try {
    await builder.send("reviewer-02", "handoff", {
      task_description: "Review NHS DTAC compliance report",
      workspace_path: "/projects/nhs-audit",
      priority: "critical",
    });
    console.log("   Handoff sent over IACP!");
  } catch (e) {
    console.log(`   API call (offline): ${(e as Error).message}`);
  }

  // 5. Negotiation
  console.log("\n5. Negotiating work...");
  try {
    await builder.negotiate(
      "reviewer-02",
      "Audit deployment config for HIPAA compliance",
      100,
      "2026-06-21T17:00:00Z"
    );
    console.log("   Negotiation sent.");
  } catch (e) {
    console.log(`   API call (offline): ${(e as Error).message}`);
  }

  // 6. Poll inbox
  console.log("\n6. Polling inbox...");
  try {
    const inbox = await reviewer.poll(undefined, 5);
    console.log(`   Messages waiting: ${inbox.length}`);
    for (const msg of inbox.slice(0, 3)) {
      const sender = msg.sender?.agent_id ?? "?";
      const intent = msg.message?.intent ?? "?";
      console.log(`   - From: ${sender} | Intent: ${intent}`);
    }
  } catch (e) {
    console.log(`   API call (offline): ${(e as Error).message}`);
  }

  // 7. Heartbeat
  console.log("\n7. Heartbeat...");
  try {
    await builder.heartbeat("healthy", 0.3);
    console.log("   Sent.");
  } catch (e) {
    console.log(`   API call (offline): ${(e as Error).message}`);
  }

  // 8. Error
  console.log("\n8. Error notification...");
  try {
    await builder.send("reviewer-02", "notify", {
      error_code: "CONTEXT_OVERFLOW",
      detail: "Task context exceeds 128K token limit",
      suggested_action: "compress_and_retry",
    }, { msgType: "error" });
    console.log("   Error sent.");
  } catch (e) {
    console.log(`   API call (offline): ${(e as Error).message}`);
  }

  console.log("\n=== Demo Complete ===");
}

main().catch(console.error);
```
