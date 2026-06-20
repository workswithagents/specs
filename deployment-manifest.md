# Agent Deployment Manifest — Cross-Layer Fleet Definition

**Version:** 1.1.0
**Status:** Published
**Layer:** Cross-layer (Agent OSI Model)
**License:** CC BY 4.0

---

## 1. Purpose

Docker Compose for AI agent fleets. Declare your entire fleet — agents, capabilities, coordination rules, compliance requirements — in one file. Deploy with one command.

---

## 2. Full Manifest

```yaml
manifest_version: "1.0.0-draft"
fleet:
  name: "regulated-nhs-fleet"
  description: "NHS Trust agent fleet — DTAC-compliant, on-prem"
  
  registry: "workswithagents.dev"
  coordination: "acp-1.0"
  
  defaults:
    model: "qwen2.5-8b-oq4"
    max_concurrent_tasks: 3
    heartbeat_interval_seconds: 30
    trust_tier_required: "reliable"

  agents:
    - id: "coordinator"
      type: "hermes"
      role: "leader"
      capabilities: ["orchestrate", "assign", "monitor"]
      max_concurrent_tasks: 1
      skills: ["kanban-orchestrator", "cron-guard"]
      
    - id: "builder"
      type: "hermes"  
      role: "worker"
      capabilities:
        - action: "build"
          target: "spfx"
        - action: "deploy"
          target: "sharepoint"
        - action: "fix"
          target: "build"
      count: 3
      skills: ["spfx-local", "spfx-heft-build-breakfix"]
      resources:
        max_tokens_per_task: 100000
        
    - id: "researcher"
      type: "hermes"
      role: "worker"
      capabilities:
        - action: "research"
          target: "general"
        - action: "research"
          target: "market"
      count: 2
      skills: ["agent-researcher", "solo-research"]
      
    - id: "compliance-officer"
      type: "hermes"
      role: "verifier"
      capabilities:
        - action: "audit"
          target: "compliance"
        - action: "verify"
          target: "dtac"
      compliance:
        layer_7: "atp-3"
        sign_off_required: true
      skills: ["executive-research-briefing-docx"]

  coordination_rules:
    leader_election:
      enabled: true
      heartbeat_interval: 30
      election_timeout: 90
    work_distribution:
      strategy: "capability_weighted"
      work_stealing: true
    conflict_resolution:
      strategy: "leader_arbitrates"

  compliance:
    regulation_refs: ["DTAC-2.1", "GDPR-Art-32", "NHS-DSP-2025"]
    audit_trail: "atp-3"
    data_classification: "confidential"
    on_prem_only: true
    
  monitoring:
    heartbeat_endpoint: "https://agent-host.example.com/v1/heartbeat"
    cron_guard: true
    trust_score_tracking: true
```

---

## 3. Minimal Manifest

For a single agent or small fleet:

```yaml
manifest_version: "1.0.0-draft"
fleet:
  name: "my-agents"
  agents:
    - id: "builder"
      type: "hermes"
      capabilities:
        - action: "build"
          target: "spfx"
```

---

→ See [implementation examples](deployment-manifest/v1.1.0/) for deploy commands and fleet management.


## 5. Agent Adoption Instructions

→ See [implementation examples](deployment-manifest/v1.1.0/) for language-specific adoption instructions.

## 6. Relationship to OSI Model

A Deployment Manifest touches all layers:

| Layer | What the manifest defines |
|-------|--------------------------|
| L1 | Model, runtime config per agent |
| L2 | Endpoints, auth requirements |
| L3 | Capabilities, registry URL |
| L4 | Handoff protocol version |
| L5 | Coordination rules, leader election |
| L6 | Skills required (quality gates) |
| L7 | Compliance rules, audit requirements |

---

*CC BY 4.0. Free to implement. Attribution required.*

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
| Python | [deployment-manifest/v1.1.0/python.md](deployment-manifest/v1.1.0/python.md) |
| TypeScript | [deployment-manifest/v1.1.0/typescript.md](deployment-manifest/v1.1.0/typescript.md) |
| cURL | [deployment-manifest/v1.1.0/curl.md](deployment-manifest/v1.1.0/curl.md) |

