# Data Chain Protocol — Accountability Protocol (DCP)

**Version:** pre-release
**Status:** Published
**Layer:** L7 — Audit
**Steward:** Community (dcp-ai-protocol)
**License:** 
**Repository:** https://github.com/dcp-ai-protocol/dcp-ai
**Specification:** https://github.com/dcp-ai-protocol/dcp-ai

## Relationship to WWA

DCP overlaps with WWA Attestation Protocol at the audit layer (L7). Both provide cryptographic audit trails for agent actions. DCP uses ed25519 signatures and Merkle tree chaining to create an immutable log of every agent action, with post-quantum cryptographic primitives (ML-KEM, ML-DSA) available for future-proofing. WWA's Attestation Protocol covers agent attestation (claiming what an agent did with verifiable receipts), while DCP focuses more on the log integrity (Merkle chaining) and quantum resistance. The two protocols address the same problem from complementary cryptographic angles.

### Problem

When autonomous agents deploy code, modify infrastructure, or process sensitive data, there is no standard way to prove what happened after the fact. Logs can be forged, timestamps can be altered, and action records can be silently deleted. If an agent makes a costly mistake or a compliance auditor asks "who did what and when," a plaintext log file is not a credible answer — you need cryptographic proof that the record hasn't been tampered with.

### Solution

DCP maintains an append-only log where every agent action is signed with ed25519 and chained into a Merkle tree. The root hash is published externally, so any third party can verify that no entry has been modified, inserted, or removed. Post-quantum cryptographic primitives (ML-KEM, ML-DSA) provide a migration path for long-lived audit trails that must remain verifiable decades into the future.

### When to use

- Compliance-heavy environments requiring non-repudiable audit trails (finance, healthcare, government)
- Multi-party systems where no single entity is trusted to maintain the log honestly
- Long-lived audit trails that must survive quantum computing advances
- Systems where agent actions have legal or financial consequences and need cryptographic proof

### When NOT to use

- Trust-based, single-organization deployments with no external audit requirements — a standard logging system is simpler
- Real-time operational monitoring — DCP is for post-hoc verification, not live alerting (use OpenTelemetry for observability)
- Low-stakes agent actions where the cost of a dispute doesn't justify the cryptographic overhead

### How it compares to similar specs

| Instead of THIS spec | When | Because |
|---|---|---|
| WWA Attestation | Agent attestation receipts with identity binding | WWA Attestation focuses on who did what with Ed25519 identity; DCP adds Merkle chaining for tamper-proof log integrity |
| WWA Auditor Verification | Verifying compliance claims against a spec | WWA Auditor Verification checks whether an agent complies with a spec; DCP proves the action log hasn't been altered after the fact |
| OpenTelemetry | Real-time observability and distributed tracing | OpenTelemetry is for live monitoring and debugging; DCP is for immutable, verifiable audit trails |

### What you lose without THIS spec

- No standard for cryptographically provable, tamper-proof agent action logs
- Auditors cannot independently verify that logs haven't been altered — trust in the log depends on trust in the operator
- No post-quantum migration path for agent audit trails
- Every compliance-sensitive system builds its own ad-hoc signing and chaining, with varying security properties

## Architecture

DCP maintains an append-only log of agent actions. Each action is signed with ed25519 and added to a Merkle tree, creating a verifiably tamper-proof chain. The root hash of each Merkle tree is published, allowing any third party to verify that no entries have been altered or removed. Post-quantum support adds ML-KEM (key encapsulation) and ML-DSA (digital signatures) as optional upgrades, making the audit trail resistant to future quantum attacks. Implementations exist in TypeScript and Rust.

## Features

- Append-only audit log of all agent actions
- ed25519 signatures for per-action cryptographic binding
- Merkle tree chaining for tamper-proof log integrity
- Post-quantum cryptography support: ML-KEM (key encapsulation), ML-DSA (signatures)
- Verifiable by any third party with the published root hash
- Implementations in TypeScript and Rust
- 23 ★ on GitHub

## Governance

Community-driven open-source project under the `dcp-ai-protocol` GitHub organization. No corporate steward. The project is in pre-release stage. License to be confirmed as the project matures. Development is open to community contributors.

## Examples

### TypeScript
```typescript
import { AuditLog, signAction, verifyChain } from "@dcp-ai/sdk";

const log = new AuditLog("agent-001");

// Sign and append an action
const entry = signAction(
  { action: "tool.invoke", tool: "terminal", command: "npm test" },
  ed25519PrivateKey
);
log.append(entry);

// Get the Merkle root for external verification
const root = log.merkleRoot();
console.log("Merkle root:", root);

// A third party verifies the chain
const isValid = verifyChain(log.entries);
console.log("Chain valid:", isValid);

// Post-quantum mode
const pqEntry = signAction(
  { action: "agent.deploy", target: "prod" },
  mlDsaPrivateKey,  // ML-DSA signature
  { kem: "ML-KEM-768" }
);
log.append(pqEntry);
```

### Rust
```rust
use dcp_ai::{AuditLog, Action, sign_action, verify_chain};

let mut log = AuditLog::new("agent-001");

// Sign and append
let entry = sign_action(
    Action::new("tool.invoke", r#"{"command": "npm test"}"#),
    &ed25519_keypair,
);
log.append(entry);

// Verify chain integrity
assert!(verify_chain(&log.entries).is_ok());
println!("Merkle root: {}", log.merkle_root());
```
