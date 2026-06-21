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
