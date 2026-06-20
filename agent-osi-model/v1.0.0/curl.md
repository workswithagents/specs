# Agent OSI Model — cURL Examples

Query and retrieve the Agent OSI Model (v1.0.0) via HTTP.

## 1. Fetch Full Model

```bash
curl https://workswithagents.dev/specs/agent-osi-model.md \
  -H "Accept: text/markdown"
```

## 2. Fetch Machine-Readable Format (YAML)

```bash
curl https://workswithagents.dev/v1/osi-model \
  -H "Accept: application/json"
```

**Expected response (200 OK):**
```json
{
  "agent_osi_version": "1.0.0",
  "layers": [
    {
      "id": 1,
      "name": "Execution",
      "responsibility": "Hardware, model runtime, tool execution",
      "interface_up": "Provides running agent process",
      "infrastructure": ["Blueprint Registry", "model config", "tool sandbox"],
      "status": "live"
    },
    {
      "id": 4,
      "name": "Session",
      "responsibility": "State transfer, context preservation, handoff between sessions",
      "interface_up": "Provides clean session state",
      "infrastructure": ["Handoff Protocol", "Context Packer"],
      "status": "in_proposal"
    }
  ]
}
```

## 3. Query Specific Layer

```bash
curl https://workswithagents.dev/v1/osi-model/layer/4 \
  -H "Accept: application/json"
```

**Expected response (200 OK):**
```json
{
  "id": 4,
  "name": "Session",
  "responsibility": "State transfer, context preservation, handoff between sessions",
  "interface_up": "Provides clean session state",
  "interface_down": "Requires target agent address (L3)",
  "infrastructure": ["Handoff Protocol", "Context Packer"],
  "debug_symptoms": ["agent lost context after restart", "handoff failed", "state corruption"],
  "status": "in_proposal"
}
```

## 4. Diagnose Symptom

```bash
curl -X POST https://workswithagents.dev/v1/osi-model/diagnose \
  -H "Content-Type: application/json" \
  -d '{
    "symptom": "agent lost context after restart"
  }'
```

**Expected response (200 OK):**
```json
{
  "symptom": "agent lost context after restart",
  "relevant_layers": [
    {
      "layer": 4,
      "name": "Session",
      "responsibility": "State transfer, context preservation, handoff between sessions"
    }
  ],
  "suggested_actions": [
    "Verify Handoff Protocol implementation",
    "Check session state serialization",
    "Review context preservation in pitfall registry"
  ]
}
```

## 5. Get Infrastructure Recommendations

```bash
curl "https://workswithagents.dev/v1/osi-model/recommend?scope=multi_agent" \
  -H "Accept: application/json"
```

**Expected response:**
```json
{
  "scope": "multi_agent",
  "required_layers": [
    {"layer": 1, "name": "Execution"},
    {"layer": 2, "name": "Communication"},
    {"layer": 3, "name": "Discovery"},
    {"layer": 4, "name": "Session"},
    {"layer": 5, "name": "Coordination"}
  ],
  "recommended_specs": [
    "Identity Protocol",
    "Capability Manifest",
    "Handoff Protocol",
    "Coordination Protocol"
  ]
}
```

## 6. Dependency Graph

```bash
curl https://workswithagents.dev/v1/osi-model/dependencies \
  -H "Accept: application/json"
```

**Expected response (200 OK):**
```json
{
  "graph": {
    "7": {"depends_on": [6], "provides": "compliance evidence"},
    "6": {"depends_on": [5], "provides": "verification results"},
    "5": {"depends_on": [4], "provides": "completed work"},
    "4": {"depends_on": [3], "provides": "clean session state"},
    "3": {"depends_on": [2], "provides": "target address + capabilities"},
    "2": {"depends_on": [1], "provides": "authenticated channels"},
    "1": {"depends_on": [], "provides": "running agent process"}
  }
}
```

## Quick Reference: Layers

| Layer | Name | Key Spec |
|-------|------|----------|
| L1 | Execution | Blueprint Registry |
| L2 | Communication | Identity Protocol, MCP, A2A |
| L3 | Discovery | Capability Manifest, Agent Registry |
| L4 | Session | Handoff Protocol |
| L5 | Coordination | Coordination Protocol, IACP |
| L6 | Verification | Agent Test Suite |
| L7 | Governance | Compliance-as-Code, Attestation |
