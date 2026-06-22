# Agent Identity Protocol — L2 Communication / L3 Discovery

**Version:** 1.1.0
**Status:** Published
**Layer:** 2/3 (Agent OSI Model)
**License:** CC BY 4.0

---

## 1. Purpose

Verifiable agent identity. "Is this agent really who it claims to be?" Cryptographic identity with key binding, signed messages, capability attestation, and revocation.

Beyond API keys. API keys prove you have a secret. Identity proves you ARE a specific agent.

### Problem
When agent A receives a message from agent B, how does it know agent B is genuine? API keys can be stolen, reused, or shared. Without cryptographic identity, impersonation is trivial — any agent can claim to be any other agent. Audit trails become meaningless because you can't prove who did what.

### Solution
The Identity Protocol binds each agent to a cryptographic key pair. Every message is signed with the sender's private key. Recipients verify signatures using the sender's public key, which is registered and can be revoked. This creates non-repudiable audit trails.

### When to use
- Agents from different trust domains need to communicate (different owners, orgs, or security boundaries)
- You need an audit trail that can be verified by a third party
- Agents handle sensitive data or financial transactions
- You're building an open ecosystem where any agent can participate
- Compliance requirements demand message-level authentication (SOX, SOC2, HIPAA)

### When NOT to use
- All agents run in a single trusted environment (same process, same VM, same Kubernetes namespace with mTLS)
- The human operator is the only verifier — no automated agent-to-agent trust decisions
- Overhead of key management outweighs the risk of impersonation (toy/side projects)

### How it compares to similar specs
| Instead of Identity Protocol | When | Because |
|----------------------------|------|---------|
| API keys / bearer tokens | You trust the transport layer to authenticate | API keys identify the caller, not the agent; they can be shared |
| mTLS | You already have a service mesh or PKI | mTLS authenticates machines, not agents; agents may move between machines |
| Attestation Protocol | You need to prove what was *done*, not who *did it* | Identity proves sender; Attestation proves actions and their compliance |

### What you lose without Identity Protocol
- Impersonation is trivial — any agent can claim any identity
- Audit trails cannot be cryptographically verified
- No mechanism to revoke a compromised agent's identity
- Cross-ecosystem trust requires a central authority
- Compliance frameworks cannot validate agent-level authentication

---

## 2. Identity Lifecycle

```
CREATE → REGISTER → ATTEST → VERIFY → ROTATE → REVOKE

CREATE:   Agent generates Ed25519 keypair
REGISTER: Agent binds public key to agent_id in registry
ATTEST:   Agent signs capability manifest with private key
VERIFY:   Other agents verify signatures against registry public key
ROTATE:   Agent generates new keypair, registers new public key (old key expires in 24h)
REVOKE:   Agent compromised → key revoked, all pending tasks reassigned
```

---

## 3. Schema

### Identity Registration

```yaml
identity_version: "1.0.0-draft"
agent_id: "hermes-spfx-builder"
public_key: "ed25519:abc123def456..."
created_at: "2026-05-05T21:00:00Z"
expires_at: null                    # null = no expiry (until rotated)

# Optional: bind to a DID
did: "did:wwa:hermes-spfx-builder"   # W3C DID format

# Optional: bind to a hardware key
hardware_binding:
  type: "tpm"
  attestation: "base64..."

# Optional: human owner
owner:
  name: "Vilius Vystartas"
  email: "agent@example.com"
  proof: "signed-challenge-response..."
```

### Signed Message

Any message from this agent carries a signature:

```yaml
message:
  agent_id: "hermes-spfx-builder"
  timestamp: "2026-05-05T21:00:00Z"
  payload:
    type: "heartbeat"
    status: "healthy"
    
signature: "ed25519:base64signature..."
```

**Verification:**
1. Fetch agent's public key from registry: `GET /v1/identity/{agent_id}`
2. Verify signature against public key + message payload
3. Check agent status (not revoked, key not expired)
4. If all pass → agent identity confirmed

---

## 4. API

```
# Register identity
POST /v1/identity/register
Body: {agent_id, public_key, [owner proof]}
→ 201 Created

# Get identity (public key + status)
GET /v1/identity/{agent_id}
→ {agent_id, public_key, status: "active"|"rotating"|"revoked", created_at}

# Verify a signed message
POST /v1/identity/verify
Body: {message, signature, agent_id}
→ {valid: true/false, agent_id, status}

# Rotate keys
POST /v1/identity/{agent_id}/rotate
Body: {new_public_key, signed_by: old_private_key}
→ {status: "rotating", old_key_expires: "2026-05-06T21:00:00Z"}

# Revoke
POST /v1/identity/{agent_id}/revoke
Body: {reason: "compromised", signed_by: private_key}
→ {status: "revoked"}
```

---

## 5. Threat Model

| Threat | Protection |
|--------|-----------|
| Impersonation (agent claims wrong ID) | Signature verification against registered public key |
| Key theft | Rotation with 24h grace period; hardware binding (TPM) for enterprise |
| Replay attack | Timestamp in signed message; messages older than 60s rejected |
| Registry compromise | Public keys only (no secrets in registry); audit log of all registrations |
| Revoked agent still operating | Heartbeat rejected; tasks reassigned by coordinator |

---

## 6. Agent Adoption Instructions

→ See [implementation examples](identity/v1.1.0/) for language-specific adoption instructions.

## 7. Relationship to OSI Model

| Layer | Identity role |
|-------|--------------|
| L2 | Signed messages over communication channels |
| L3 | Identity registered in discovery layer |
| L5 | Coordinator verifies identities before delegating |
| L7 | Identity required for audit trail attribution |

---

## 8. Standards Alignment

- **Key format:** Ed25519 (RFC 8032)
- **DID:** W3C DID Core (did:wwa: method)
- **Signature:** EdDSA (Ed25519)
- **Hardware binding:** TPM 2.0 attestation (optional, enterprise)

---

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.1.0 | 2026-06-20 | Moved inline implementation examples to versioned example directories. Spec definitions unchanged. |
| 1.0.0 | — | Initial specification. |

## Examples

Implementation examples for this version:

| Language | File |
|----------|------|
| Python | [identity/v1.1.0/python.md](identity/v1.1.0/python.md) |
| TypeScript | [identity/v1.1.0/typescript.md](identity/v1.1.0/typescript.md) |
| cURL | [identity/v1.1.0/curl.md](identity/v1.1.0/curl.md) |

---

*CC BY 4.0. Free to implement. Attribution required.*
