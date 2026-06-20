# Agent Attestation Protocol — Layer 7

**Version:** 1.1.0
**Status:** Published
**Layer:** 7 — Audit (Agent OSI Model)
**License:** CC BY 4.0

## 1. Purpose

Define how an AI agent generates a cryptographically signed, tamper-evident attestation that proves: what was generated, from what inputs, applying which compliance standards, at a specific time.

This is the **trust layer** for agent-generated code in regulated industries. No black boxes. No trust in the operator.

## 2. Design Principles

- **Inputs → Outputs, hashed.** Every input to the agent and every output file is SHA-256 hashed. The hash chain proves the output matches the inputs without re-running the generation.
- **Signed, not claimed.** Every attestation carries an Ed25519 signature from the agent's key. Signature is verifiable without trusting the operator.
- **Immutable timestamp.** Attestation hash is optionally published on-chain (Arbitrum/Base via Mycelium Trails) for tamper-evident timestamping.
- **Deterministic replay.** Same inputs, same agent version → same outputs. Anyone can verify.
- **Framework-agnostic.** Any MCP-compatible agent can produce attested output.

## 3. Attestation Schema

```json
{
  "$schema": "https://workswithagents.dev/specs/attestation-protocol.json",
  "protocol_version": "1.0.0",
  "attestation_id": "uuid",
  "session_id": "uuid",
  "agent_id": "wwa-scaffold-v1.0.0",
  "agent_version": "1.0.0",
  "agent_public_key": "ed25519:abc123...",
  "timestamp": "2026-05-10T15:00:00Z",

  "inputs": {
    "description": "MOD training tracker with employee records",
    "component_type": "webpart-react",
    "operation": "add",
    "clarification_rounds": 1,
    "clarification_chain_ref": "clarification://session/xxx",

    "standards_selected": ["jsp-440", "wcag-2-2-aa"],
    "standards_auto_covered": {
      "jsp-440": [],
      "wcag-2-2-aa": []
    },
    "overlaps_detected": {
      "jsp-440": {"partially_covers": ["nato-stanag"]}
    },
    "languages": ["en-us", "en-gb"],
    "libraries": ["pnp-sp", "dayjs"],
    "data_storage": "properties",
    "api_choice": "rest",
    "spo_theme": true,
    "real_build": false,

    "planner_version": "v1.0.0",
    "input_hash": "sha256:def789..."
  },

  "outputs": {
    "total_files": 24,
    "files_created": 20,
    "files_updated": 4,
    "compliance_libraries": 6,
    "locale_files": 2,
    "audit_file": "COMPLIANCE-AUDIT.md",
    "output_path": "src/webparts/trainingTracker/",

    "file_hashes": [
      {
        "path": "src/webparts/trainingTracker/TrainingTrackerWebPart.ts",
        "sha256": "sha256:X1a2b3...",
        "action": "created",
        "compliance_relevant": true,
        "standards_applied": ["jsp-440", "wcag-2-2-aa"]
      },
      {
        "path": "src/webparts/trainingTracker/TrainingTrackerWebPart.manifest.json",
        "sha256": "sha256:Y4c5d6...",
        "action": "created",
        "compliance_relevant": false
      }
    ],
    "output_hash": "sha256:MERKLE_ROOT_OF_ALL_FILE_HASHES",
    "build_result": {
      "exit_code": 0,
      "errors": 0,
      "warnings": 0,
      "build_log_hash": "sha256:build_log_hash..."
    }
  },

  "compliance_claims": [
    {
      "standard": "jsp-440",
      "status": "selected",
      "rationale": "keyword_preselection: 'MOD' in description",
      "files_checked": 3,
      "hash_subtree": "sha256:compliant_subtree_hash..."
    }
  ],

  "deterministic": {
    "seed": null,
    "random_free": true,
    "agent_version_pinned": "wwa-scaffold-mcp==1.0.0",
    "reproducible_command": "echo '{\"description\":\"MOD training tracker...\"}' | python3.11 -m wwa_scaffold_mcp.server",
    "expected_output_hash": "sha256:MERKLE_ROOT_OF_ALL_FILE_HASHES"
  },

  "signature": "ed25519:signature_of_attestation_id+timestamp+output_hash..."
}
```

## 4. Deterministic Generation (Non-Negotiable)

For an attestation to be verifiable, generation MUST be deterministic:

| Rule | Current | Attested mode |
|------|---------|---------------|
| No `Math.random()` | Used in sleep/simulation timers | Removed — fixed durations or seed-based |
| No non-deterministic I/O | Reading filesystem state | Input snapshot hashed before generation |
| No external API calls | N/A in scaffold | All data embedded in agent |
| Fixed template versions | Templates loaded from fileTemplates.ts | Template hash included in attestation |
| Agent version pinned | N/A | Version locked in attestation |

**Reproducibility test:**
→ See [implementation examples](attestation-protocol/v1.1.0/) for reproducibility testing commands and verification workflows.

## 5. Git Signed Commits

Every attested scaffold MUST produce a signed git commit:

→ See [implementation examples](attestation-protocol/v1.1.0/) for signed commit examples and attestation workflows.

The `-S` flag uses GPG or SSH signing. The agent's signing key is distinct from the developer's personal key — it's the agent's Ed25519 identity key from the WWA Identity Protocol.

## 6. On-Chain Timestamp (Optional — Mycelium Trails)

For regulatory-grade immutability, the attestation hash is published to Arbitrum/Base:

```
SHA-256(signed_attestation) → attestation_hash
  ↓
Mycelium Trails: publish TrailRecord(attestation_hash)
  ↓
L2 transaction is now immutable with block timestamp
  ↓
Auditor verifies: hash matches on-chain record at time T
```

**Why L2:** Cheaper than L1, sufficient for audit trails. The hash alone proves integrity; the chain proves "this attestation existed at or before time T."

## 7. MCP Tools

### `wwa_attest_sign`

Sign an attestation with the agent's Ed25519 key.

```
Input:  attestation_json (full attestation object)
Output: {attestation_id, timestamp, output_hash, signature}
```

### `wwa_attest_verify`

Verify an attestation: signature valid + hash matches + reproducible.

```
Input:  attestation_json or attestation_id
Output: {valid: true|false, checks: {signature, hash_chain, reproducibility, clarification_chain}}
```

### `wwa_attest_audit`

Return full attestation + clarification chain for an auditor.

```
Input:  session_id
Output: {attestation, clarification_chain, all_signatures, on_chain_ref (if published)}
```

### `wwa_attest_git_commit`

Generate a signed git commit with structured attestation message.

```
Input:  attestation_id, repo_path, agent_gpg_key_id
Output: {commit_hash, signed: true, attestation_ref_in_message}
```

### `wwa_attest_timestamp`

Publish attestation hash to L2 for immutable timestamp.

```
Input:  attestation_id, chain ("arbitrum"|"base")
Output: {tx_hash, block_number, timestamp, explorer_url}
```

### `wwa_scaffold_attest`

Full end-to-end attested scaffold: generate → attest → sign → commit.

```
Input:  description, standards[], languages[], etc. (same as wwa_scaffold_plan)
        + auto_attest: true
        + auto_commit: true
        + auto_timestamp: false (optional L2)
Output: {attestation_id, commit_hash, signature, output_hash, verification_url}
```

## 8. Auditor Verification Flow

```
1. Clone repo at attested commit:
   git clone <repo> && git checkout <commit_hash>

2. Verify commit signature:
   git verify-commit <commit_hash>
   → Good signature from agent key X ✓

3. Extract attestation:
   git show <commit_hash> -- format="%B" | grep "Attestation:"
   → sha256:abc123...

4. Verify attestation via MCP:
   wwa_attest_verify({attestation_id: "sha256:abc123..."})
   → Signature valid ✓  Hash chain matches ✓  Reproducible ✓

5. Optional: check on-chain timestamp:
   wwa_attest_audit({session_id: "..."})
   → On-chain: Arbitrum tx 0x... block 12345678 at 2026-05-10T15:05:00Z ✓

Auditor conclusion:
   "Agent X generated these 24 files with JSP 440 + WCAG 2.2 AA.
    No modifications after generation. Zero build errors.
    Verifiable without trusting the operator or the agent infrastructure."
```

## 9. Relation to Other Protocols

| Protocol | Relationship |
|----------|-------------|
| Identity Protocol (#15) | Agent Ed25519 key used for attestation signing |
| Clarification Protocol (#17) | Attestation references clarification chain — "generated after 1 round of clarification" |
| Handoff Protocol (#8) | Attestation included in handoff context pack |
| SLA Framework (#12) | Attestation counts as "validated output" for SLA metrics |

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
| Python | [attestation-protocol/v1.1.0/python.md](attestation-protocol/v1.1.0/python.md) |
| TypeScript | [attestation-protocol/v1.1.0/typescript.md](attestation-protocol/v1.1.0/typescript.md) |
| cURL | [attestation-protocol/v1.1.0/curl.md](attestation-protocol/v1.1.0/curl.md) |

