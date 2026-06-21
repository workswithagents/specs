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
