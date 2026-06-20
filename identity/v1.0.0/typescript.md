# Identity Protocol — TypeScript Example

Complete TypeScript implementation of the Identity Protocol (v1.0.0).

```typescript
/**
 * Identity Protocol v1.0.0 — TypeScript Reference Implementation
 *
 * Full lifecycle: CREATE → REGISTER → ATTEST → VERIFY → ROTATE → REVOKE
 * Uses Web Crypto API (subtle) for Ed25519 — no external deps (Node 20+).
 */
import { subtle } from "node:crypto";

// ── Types ────────────────────────────────────────────────────────

interface KeyPair {
  agentId: string;
  publicKeyHex: string;
  privateKeyRaw: ArrayBuffer;
}

interface SignedMessage {
  message: {
    agent_id: string;
    timestamp: string;
    payload: Record<string, unknown>;
  };
  signature: string; // "ed25519:hex..."
}

interface Identity {
  agent_id: string;
  public_key: string;
  status: "active" | "rotating" | "revoked";
  created_at: string;
  expires_at: string | null;
  owner?: {
    name: string;
    email: string;
  };
}

// ── Client ───────────────────────────────────────────────────────

class IdentityClient {
  private agentId: string;
  private apiBase: string;
  private privateKey: CryptoKey | null = null;
  private publicKeyHex: string = "";

  constructor(agentId: string, apiBase: string = "https://workswithagents.dev") {
    this.agentId = agentId;
    this.apiBase = apiBase.replace(/\/$/, "");
  }

  private async request<T>(method: string, path: string, body?: Record<string, unknown>): Promise<T> {
    const url = `${this.apiBase}${path}`;
    const options: RequestInit = {
      method,
      headers: { "Content-Type": "application/json" },
    };
    if (body) options.body = JSON.stringify(body);
    const res = await fetch(url, options);
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: "unknown" }));
      throw new Error(`Identity error (${res.status}): ${err.detail}`);
    }
    return res.json() as Promise<T>;
  }

  // ── CREATE: Generate Ed25519 keypair ───────────────────────────

  async createKeypair(): Promise<{ agentId: string; publicKeyHex: string }> {
    const keyPair = await subtle.generateKey(
      { name: "Ed25519" },
      true, // extractable
      ["sign", "verify"]
    ) as CryptoKeyPair;

    this.privateKey = keyPair.privateKey;

    // Export public key as raw bytes
    const pubRaw = await subtle.exportKey("raw", keyPair.publicKey);
    this.publicKeyHex = Buffer.from(pubRaw).toString("hex");

    return {
      agentId: this.agentId,
      publicKeyHex: this.publicKeyHex,
    };
  }

  async exportPrivateKeyHex(): Promise<string> {
    if (!this.privateKey) throw new Error("No keypair. Call createKeypair() first.");
    const raw = await subtle.exportKey("raw", this.privateKey);
    return Buffer.from(raw).toString("hex");
  }

  // ── REGISTER ───────────────────────────────────────────────────

  async register(owner?: { name: string; email: string }): Promise<Identity> {
    const body: Record<string, unknown> = {
      agent_id: this.agentId,
      public_key: this.publicKeyHex,
      identity_version: "1.0.0",
    };
    if (owner) body.owner = owner;
    return this.request("POST", "/v1/identity/register", body);
  }

  // ── SIGN ───────────────────────────────────────────────────────

  async signMessage(payload: Record<string, unknown>): Promise<SignedMessage> {
    if (!this.privateKey) throw new Error("No keypair. Call createKeypair() first.");

    const message = {
      agent_id: this.agentId,
      timestamp: new Date().toISOString(),
      payload,
    };

    const messageBytes = new TextEncoder().encode(
      JSON.stringify(message, Object.keys(message).sort())
    );

    const sigRaw = await subtle.sign("Ed25519", this.privateKey, messageBytes);
    const sigHex = Buffer.from(sigRaw).toString("hex");

    return {
      message,
      signature: `ed25519:${sigHex}`,
    };
  }

  // ── VERIFY ─────────────────────────────────────────────────────

  async verifyIdentity(signed: SignedMessage, otherAgentId: string): Promise<{
    valid: boolean;
    agent_id: string;
    status?: string;
    reason?: string;
  }> {
    // Fetch public key
    const identity = await this.request<Identity>("GET", `/v1/identity/${otherAgentId}`);
    const pubKeyBytes = Buffer.from(identity.public_key, "hex");

    const publicKey = await subtle.importKey(
      "raw",
      pubKeyBytes,
      { name: "Ed25519" },
      true,
      ["verify"]
    );

    const messageBytes = new TextEncoder().encode(
      JSON.stringify(signed.message, Object.keys(signed.message).sort())
    );

    const sigHex = signed.signature.replace(/^ed25519:/, "");
    const sigBytes = Buffer.from(sigHex, "hex");

    try {
      const valid = await subtle.verify("Ed25519", publicKey, sigBytes, messageBytes);
      return {
        valid,
        agent_id: otherAgentId,
        status: identity.status,
      };
    } catch {
      return { valid: false, agent_id: otherAgentId, reason: "verification_error" };
    }
  }

  // ── ROTATE ─────────────────────────────────────────────────────

  async rotateKeypair(): Promise<{ status: string; old_key_expires?: string }> {
    if (!this.privateKey) throw new Error("No keypair.");

    const oldPriv = this.privateKey;
    const newPair = await this.createKeypair();

    const rotationMsg = {
      agent_id: this.agentId,
      timestamp: Math.floor(Date.now() / 1000),
      payload: {
        type: "key_rotation",
        new_public_key: this.publicKeyHex,
      },
    };

    const msgBytes = new TextEncoder().encode(
      JSON.stringify(rotationMsg, Object.keys(rotationMsg).sort())
    );
    const sigRaw = await subtle.sign("Ed25519", oldPriv, msgBytes);
    const sigHex = Buffer.from(sigRaw).toString("hex");

    return this.request("POST", `/v1/identity/${this.agentId}/rotate`, {
      new_public_key: newPair.publicKeyHex,
      signed_by: `ed25519:${sigHex}`,
      rotation_message: rotationMsg,
    });
  }

  // ── REVOKE ─────────────────────────────────────────────────────

  async revoke(reason: string = "compromised"): Promise<{ status: string }> {
    if (!this.privateKey) throw new Error("No keypair.");

    const revokeMsg = {
      agent_id: this.agentId,
      timestamp: Math.floor(Date.now() / 1000),
      payload: { type: "revocation", reason },
    };

    const msgBytes = new TextEncoder().encode(
      JSON.stringify(revokeMsg, Object.keys(revokeMsg).sort())
    );
    const sigRaw = await subtle.sign("Ed25519", this.privateKey, msgBytes);
    const sigHex = Buffer.from(sigRaw).toString("hex");

    return this.request("POST", `/v1/identity/${this.agentId}/revoke`, {
      reason,
      signed_by: `ed25519:${sigHex}`,
    });
  }

  // ── LOOKUP ─────────────────────────────────────────────────────

  async lookup(targetAgentId: string): Promise<Identity> {
    return this.request("GET", `/v1/identity/${targetAgentId}`);
  }
}

// ── Demo ─────────────────────────────────────────────────────────

async function main() {
  console.log("=== Identity Protocol v1.0.0 Demo ===\n");

  // Step 1: CREATE
  const alice = new IdentityClient("alice-builder-01");
  const keypair = await alice.createKeypair();
  console.log("1. Keypair generated:");
  console.log(`   Agent:    ${keypair.agentId}`);
  console.log(`   Pub key:  ${keypair.publicKeyHex.slice(0, 40)}...`);

  // Step 2: REGISTER
  console.log("\n2. Registering identity...");
  try {
    const result = await alice.register({
      name: "Alice Engineer",
      email: "alice@workswithagents.dev",
    });
    console.log(`   Status:  ${result.status}`);
  } catch (e) {
    console.log(`   API call (offline): ${(e as Error).message}`);
  }

  // Step 3: SIGN
  console.log("\n3. Signing a heartbeat message...");
  const signed = await alice.signMessage({
    type: "heartbeat",
    status: "healthy",
    load: 0.3,
  });
  console.log(`   Signature: ${signed.signature.slice(0, 50)}...`);

  // Step 4: VERIFY
  console.log("\n4. Verifying another agent...");
  const bob = new IdentityClient("bob-reviewer-02");
  await bob.createKeypair();
  const bobSigned = await bob.signMessage({ type: "query", question: "Review ready?" });

  try {
    const verification = await alice.verifyIdentity(bobSigned, "bob-reviewer-02");
    console.log(`   Valid:  ${verification.valid}`);
    console.log(`   Agent:  ${verification.agent_id}`);
  } catch (e) {
    console.log(`   API call (offline): ${(e as Error).message}`);
  }

  // Step 5: LOOKUP
  console.log("\n5. Looking up identity...");
  try {
    const id = await alice.lookup("bob-reviewer-02");
    console.log(`   Status: ${id.status}`);
    console.log(`   Key:    ${id.public_key?.slice(0, 40)}...`);
  } catch (e) {
    console.log(`   API call (offline): ${(e as Error).message}`);
  }

  // Step 6: ROTATE
  console.log("\n6. Rotating keys...");
  try {
    const rotation = await alice.rotateKeypair();
    console.log(`   Status: ${rotation.status}`);
  } catch (e) {
    console.log(`   API call (offline): ${(e as Error).message}`);
  }

  // Step 7: REVOKE
  console.log("\n7. Revocation (demo)...");
  console.log(`   POST /v1/identity/${alice["agentId"]}/revoke`);
  console.log('   Body: {"reason": "compromised"}');

  console.log("\n=== Lifecycle Complete ===");
}

main().catch(console.error);
```
