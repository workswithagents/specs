# Local-First Certification (Cross-Cutting)

**Version:** 1.0.0
**Status:** Published
**Layer:** Cross-Cutting (L0-L7)
**License:** CC BY 4.0

## Abstract

Local-First Certification verifies that an AI agent or agent infrastructure operates entirely on-premises without external API dependencies. Certified agents guarantee data sovereignty, offline operation, and zero third-party data transmission.

### Problem
Many organizations (healthcare, defence, intelligence) cannot send data to external API providers. But there's no standard way to verify that an agent claiming "local-first" actually runs locally. Vendors can claim anything. Without certification, procurement teams must trust marketing claims or manually audit every agent's network traffic.

### Solution
A three-tier certification (Local Inference → Local Data → Fully Air-Gapped) verified by automated network capture during operation. Any outbound call to non-approved endpoints fails certification. Certified agents receive a verifiable badge. Procurement teams can require a specific certification level instead of auditing every agent.

### When to use
- Privacy-sensitive environments where data must never leave the device
- Air-gapped or isolated networks with zero internet connectivity
- Edge devices and on-prem deployments where cloud APIs are unavailable
- Procurement requiring proof of local operation before purchase

### When NOT to use
- Cloud-based agents where data inherently must leave the device
- No privacy or air-gap requirements — certification adds no value
- You only need agent identity verification — use Identity Protocol
- You need ephemeral computation (not persistent local) — use ECP

### How it compares to similar specs
| Instead of THIS | When | Because |
|---|---|---|
| Identity Protocol | Verifying who an agent is | Identity proves cryptographic identity; Local-First proves the agent operates without external dependencies |
| ECP (Ephemeral Computation) | Stateless, short-lived computation | ECP is about ephemeral sessions; Local-First is about persistent, offline-capable operation |

### What you lose without THIS
- No standard way to verify an agent's "local-first" claim — must trust vendor marketing
- Procurement teams can't require a specific local operation level in RFPs
- No automated certification — every agent must be manually audited for network traffic
- Air-gapped and privacy-sensitive deployments can't verify agents meet requirements

## Certification Levels

| Level | Name | Requirements |
|-------|------|-------------|
| L1 | **Local Inference** | Model runs locally. No cloud API calls for inference. |
| L2 | **Local Data** | All data processing happens on-prem. No external storage. |
| L3 | **Fully Air-Gapped** | Zero outbound connections. Operates on isolated network. |

## Verification

1. Agent declares target certification level
2. Automated audit runs network capture during operation
3. Any outbound call to non-approved endpoints fails certification
4. Certified agents receive `local-first.svg` badge

## Badge

`![Local-First Certified](https://workswithagents.io/badges/local-first.svg)`

## Related Protocols

- Identity Protocol (L2) — agents must have cryptographic identity before certification
- Trust Score (L3) — Local-First certification contributes positively to trust score
- Onboarding Protocol (L1) — certification is part of agent provisioning

---

## Examples

Implementation examples for this version:

| Language | File |
|----------|------|
| Python | [local-first/v1.0.0/python.md](local-first/v1.0.0/python.md) |
| TypeScript | [local-first/v1.0.0/typescript.md](local-first/v1.0.0/typescript.md) |
| cURL | [local-first/v1.0.0/curl.md](local-first/v1.0.0/curl.md) |

