# Compliance-as-Code — L7 Governance

**Version:** 1.1.0
**Status:** Published
**Layer:** 7 (Agent OSI Model)
**License:** CC BY 4.0

---

## 1. Purpose

Turn regulation into executable validation rules that AI agents can run against. Not documentation. Not checklists. Actual code that says "this deployment passes DTAC" or "this action violates FCA Senior Managers Regime."

Regulators publish PDFs. We translate them into YAML rules that agents validate against.

---

## 2. Regulation → Rule Translation

| Regulation | Published as | We translate to |
|------------|-------------|-----------------|
| NHS DTAC | 78-page PDF | `dtac-compliance.yaml` — 12 rule categories |
| FCA Senior Managers Regime | 200+ pages | `fca-smr.yaml` — 8 rule categories |
| GDS Service Standard | 14 points | `gds-standard.yaml` — 14 rules |
| GDPR (UK DPA 2018) | Legislation | `gdpr-compliance.yaml` — 7 rule categories |
| SOC 2 | Trust Service Criteria | `soc2-compliance.yaml` — 5 categories |
| ISO 27001 | Standard document | `iso27001-compliance.yaml` — 14 control categories |

---

## 3. Rule Schema

Each compliance rule is machine-readable YAML that agents validate against:

```yaml
compliance_version: "1.0.0-draft"
regulation: "NHS DTAC"
version: "2.1"
domain: "healthcare"

rules:
  - id: "DTAC-2.1.3"
    name: "Clinical Safety"
    description: "All agent actions affecting clinical data must have audit trail and rollback"
    severity: "critical"
    
    # When to check
    trigger:
      events: ["deploy", "data_access", "data_modify"]
      data_classification: ["confidential", "restricted"]
      
    # What to check
    validation:
      - field: "action.guarantee_level"
        operator: "equals"
        value: "atp-3"
        message: "Clinical data actions must use ATP-3 (Exactly-Once with rollback)"
        
      - field: "compliance.audit_trail_id"
        operator: "exists"
        message: "All clinical data actions must have an audit trail ID"
        
      - field: "compliance.sign_off_required"
        operator: "equals"
        value: true
        message: "Clinical data actions require human sign-off"
        
      - field: "reversible"
        operator: "equals"
        value: true
        message: "Clinical data actions must be reversible (rollback required)"
        
      - field: "compliance.clinical_safety_ref"
        operator: "exists"
        message: "Clinical safety case reference required"
    
    # Evidence needed
    evidence:
      - type: "audit_log"
        description: "Immutable audit trail of action"
      - type: "sign_off"
        description: "Named clinical safety officer approval"
      - type: "dpia_ref"
        description: "Data Protection Impact Assessment reference"

  - id: "DTAC-3.2.1"
    name: "Data Residency"
    description: "Patient data must not leave UK data centres"
    severity: "critical"
    
    trigger:
      data_classification: ["confidential", "restricted"]
      
    validation:
      - field: "action.parameters.region"
        operator: "in"
        value: ["uk", "eu"]
        message: "Data processing must occur in UK or EU regions"
        
      - field: "action.parameters.on_prem_only"
        operator: "equals"
        value: true
        message: "On-prem deployment required for patient data processing"
```

---

## 3.a Agent Compliance Manifest

A Compliance Manifest is a JSON document that an agent fleet carries to declare its regulatory posture. It is loaded at session start and validated before every regulated action.

```yaml
compliance_manifest:
  manifest_id: "cm_a1b2c3d4"
  version: "1.1.0"
  fleet_id: "fleet-nhs-trust-a"
  generated_at: "2026-06-19T12:00:00Z"

  # ── Audit Level ──────────────────────────────────────────────
  # Controls how much execution evidence is retained.
  #   log        — Basic action log (who, what, when)
  #   hash       — All actions hashed into an append-only digest chain
  #   full-replay — Every action, input, output, and decision recorded
  audit_level: "hash"

  # ── Data Sovereignty ─────────────────────────────────────────
  # Restricts which regions and jurisdictions data can be processed in.
  data_sovereignty:
    allowed_regions: ["uk", "eu"]
    forbidden_regions: ["us", "cn", "ru"]
    data_classification_boundary:
      confidential: { allowed_regions: ["uk"], requires_on_prem: true }
      restricted:   { allowed_regions: ["uk"], requires_on_prem: true }
      internal:     { allowed_regions: ["uk", "eu"], requires_on_prem: false }
      public:       { allowed_regions: "*", requires_on_prem: false }

  # ── Human-in-the-Loop ───────────────────────────────────────
  # Defines which operations require human approval before execution.
  human_in_the_loop:
    enabled: true
    triggers:
      - action: "deploy"
        required_approvers: 1
        timeout_seconds: 3600
      - action: "data_access"
        data_classification: ["confidential", "restricted"]
        required_approvers: 1
      - action: "data_modify"
        data_classification: ["confidential", "restricted"]
        required_approvers: 2
      - action: "spend"
        threshold_usd: 100
        required_approvers: 1
      - action: "contract_sign"
        required_approvers: 2
        legal_required: true
    auto_approve:
      - action: "data_access"
        data_classification: ["internal", "public"]
      - action: "inference"
        max_cost_usd: 5.00

  # ── Applicable regulations ───────────────────────────────────
  regulations:
    - id: "dtac-v2.1"
      mandatory: true
    - id: "gdpr"
      jurisdiction: "uk"
      mandatory: true
```

### Schema Reference

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `manifest_id` | string | yes | Unique manifest identifier |
| `version` | string | yes | Schema version (`1.0.0`) |
| `audit_level` | enum | yes | `log` \| `hash` \| `full-replay` |
| `data_sovereignty.allowed_regions` | string[] | yes | Permitted processing regions |
| `data_sovereignty.forbidden_regions` | string[] | yes | Blocked processing regions |
| `data_sovereignty.data_classification_boundary` | object | yes | Per-classification region+on-prem rules |
| `human_in_the_loop.enabled` | boolean | yes | Master switch for HITL |
| `human_in_the_loop.triggers` | object[] | no | Operations requiring human approval |
| `human_in_the_loop.auto_approve` | object[] | no | Operations exempt from HITL |
| `regulations` | object[] | yes | Applicable regulation packs |

### Validation Pseudocode

```python
def validate_action_against_manifest(action, manifest):
    # 1. Check audit level
    if manifest.audit_level == "full-replay":
        assert "full_action_log" in action, "Full replay requires complete action trace"
    
    # 2. Check data sovereignty
    region = action.get("region", "uk")
    if region in manifest.data_sovereignty.forbidden_regions:
        raise ComplianceViolation(f"Region {region} is forbidden")
    if region not in manifest.data_sovereignty.allowed_regions:
        raise ComplianceViolation(f"Region {region} not in allowed set")
    
    # 3. Check classification boundaries
    classification = action.get("data_classification", "public")
    boundaries = manifest.data_sovereignty.data_classification_boundary
    if classification in boundaries:
        rule = boundaries[classification]
        if rule.get("requires_on_prem") and not action.get("is_on_prem"):
            raise ComplianceViolation("On-prem deployment required")
        if rule.get("allowed_regions") != "*":
            if region not in rule["allowed_regions"]:
                raise ComplianceViolation(f"{classification} data not allowed in {region}")
    
    # 4. Check human-in-the-loop triggers
    if manifest.human_in_the_loop.enabled:
        for trigger in manifest.human_in_the_loop.triggers:
            if matches_trigger(action, trigger):
                if not action.get("human_approved"):
                    raise ComplianceViolation(f"Human approval required: {trigger.action}")
    
    return True
```

---


---

## 5. Built-In Regulation Packs

| Pack | Rules | Status |
|------|-------|--------|
| NHS DTAC v2.1 | 12 rule categories | Spec written |
| FCA SMR | 8 rule categories | Planned |
| GDS Service Standard | 14 rules | Planned |
| GDPR / UK DPA 2018 | 7 rule categories | Planned |
| SOC 2 Type II | 5 categories | Planned |
| ISO 27001:2022 | 14 control categories | Planned |

---

## 6. API

```
# List available regulation packs
GET /v1/compliance/packs
→ ["dtac-v2.1", "fca-smr", "gdpr", "gds-standard", ...]

# Get a specific regulation pack
GET /v1/compliance/packs/dtac-v2.1
→ Full YAML rule set

# Validate an action against a regulation
POST /v1/compliance/validate
Body: {regulation: "dtac-v2.1", action: {...}}
→ {passed: false, violations: [...], evidence_required: [...]}

# Generate compliance evidence for an assessment
POST /v1/compliance/evidence
Body: {regulation: "dtac-v2.1", fleet_id: "nhs-fleet", period: "2026-05"}
→ {report: "...", evidence: [...], ready_for_submission: true}
```

---

## 7. Agent Adoption Instructions

→ See [implementation examples](compliance-as-code/v1.1.0/) for language-specific adoption instructions.

## 8. Relationship to OSI Model

| Layer | Compliance role |
|-------|----------------|
| L5 Coordination | Compliance rules restrict which agents can handle regulated tasks |
| L6 Verification | Compliance validation is a quality gate |
| L7 Governance | **This is Layer 7.** Compliance-as-Code IS the governance execution layer. |
| Transaction Protocol | ATP-3 actions validated against compliance rules before execution |

---

## 9. Why This Is a Moat

- **Regulatory capture.** Once NHS procurement templates reference "DTAC Compliance-as-Code validation," every vendor needs it.
- **Translation barrier.** Regulators publish PDFs. Coders don't read PDFs. We translate once, validate forever.
- **Zero competitors.** Nobody is turning regulation into executable validation rules for AI agents. AgentOps.ai has "audit trail" — that's a log viewer, not compliance validation.
- **Willingness to pay.** NHS trusts spend £millions on compliance. A £2000/mo tool that auto-generates DTAC evidence is a rounding error.

---

*CC BY 4.0. Regulation packs: free to use. Custom regulation translation: enterprise service.*

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
| Python | [compliance-as-code/v1.1.0/python.md](compliance-as-code/v1.1.0/python.md) |
| TypeScript | [compliance-as-code/v1.1.0/typescript.md](compliance-as-code/v1.1.0/typescript.md) |
| cURL | [compliance-as-code/v1.1.0/curl.md](compliance-as-code/v1.1.0/curl.md) |

