# Agent OSI Model — Python Example

Complete Python implementation for working with the Agent OSI Model (v1.0.0).

```python
"""
Agent OSI Model v1.0.0 — Python Reference Implementation

Utilities for working with the 7-layer agent infrastructure model:
  - Layer lookup and validation
  - Debugging assistant (symptom → layer mapping)
  - Infrastructure builder guidance
  - Machine-readable format parsing
"""
from typing import Optional

# ── Layer Definitions ─────────────────────────────────────────────

LAYERS = {
    1: {
        "name": "Execution",
        "responsibility": "Hardware, model runtime, tool execution",
        "interface_up": "Provides running agent process",
        "examples": "Blueprint Registry, model config, tool sandbox",
        "debug": ["agent won't start", "model crash", "out of memory"],
        "status": "live"
    },
    2: {
        "name": "Communication",
        "responsibility": "Agent messaging, authentication, API contracts",
        "interface_up": "Provides authenticated channels",
        "examples": "MCP, A2A, OpenAPI 3.1, Credential Proxy",
        "debug": ["agent can't authenticate", "API call fails", "TLS error"],
        "status": "live"
    },
    3: {
        "name": "Discovery",
        "responsibility": "Agent registry, capability advertisement, service location",
        "interface_up": "Provides target agent address and capabilities",
        "examples": "llms.txt, Capability Manifest, Agent Registry",
        "debug": ["agent can't find service", "unknown capability", "peer not found"],
        "status": "partial"
    },
    4: {
        "name": "Session",
        "responsibility": "State transfer, context preservation, handoff between sessions",
        "interface_up": "Provides clean session state",
        "examples": "Handoff Protocol, Context Packer",
        "debug": ["agent lost context after restart", "handoff failed", "state corruption"],
        "status": "in_proposal"
    },
    5: {
        "name": "Coordination",
        "responsibility": "Work distribution, consensus, conflict resolution, leader election",
        "interface_up": "Provides completed work",
        "examples": "Coordination Protocol, Cron Guard",
        "debug": ["two agents overwrote same file", "race condition", "dead agent"],
        "status": "spec_written"
    },
    6: {
        "name": "Verification",
        "responsibility": "Testing, evaluation, quality gates, regression detection",
        "interface_up": "Provides verification results",
        "examples": "Agent Test Suite, Pitfall Registry, Quality Gates",
        "debug": ["agent produces wrong output", "regression", "test failure"],
        "status": "partial"
    },
    7: {
        "name": "Governance",
        "responsibility": "Audit, compliance, sign-off, regulatory alignment",
        "interface_up": "Provides compliance evidence",
        "examples": "Regulated Handoff, Compliance-as-Code, Audit Trail",
        "debug": ["compliance blocked deployment", "audit failure", "missing sign-off"],
        "status": "planned"
    }
}


class AgentOSIModel:
    """Utility class for working with the Agent OSI Model."""

    @staticmethod
    def get_layer(layer_id: int) -> Optional[dict]:
        """Get full layer definition by numeric ID (1-7)."""
        return LAYERS.get(layer_id)

    @staticmethod
    def diagnose(symptom: str) -> list[dict]:
        """Given a symptom, return relevant layers to investigate."""
        symptom_lower = symptom.lower()
        matches = []
        for layer_id, layer in LAYERS.items():
            for keyword in layer["debug"]:
                if keyword.lower() in symptom_lower:
                    matches.append({"layer": layer_id, "name": layer["name"],
                                    "responsibility": layer["responsibility"]})
                    break
        return matches

    @staticmethod
    def infrastructure_guide(scope: str) -> list[dict]:
        """Return which layers to focus on for a given scope."""
        scope_map = {
            "local": [1, 2, 4],
            "multi_agent": [1, 2, 3, 4, 5],
            "enterprise": [1, 2, 3, 4, 5, 6, 7],
            "regulated": [1, 2, 3, 4, 5, 6, 7],
        }
        layer_ids = scope_map.get(scope, [1, 2, 4])
        return [{"layer": lid, "name": LAYERS[lid]["name"],
                 "responsibility": LAYERS[lid]["responsibility"]}
                for lid in layer_ids]

    @staticmethod
    def to_yaml() -> str:
        """Serialize model as structured YAML for agent consumption."""
        import json
        layers_yaml = []
        for lid in range(1, 8):
            l = LAYERS[lid]
            layers_yaml.append({
                "id": lid,
                "name": l["name"],
                "responsibility": l["responsibility"],
                "interface_up": l["interface_up"],
                "infrastructure": l["examples"].split(", "),
                "status": l["status"]
            })
        return json.dumps({"agent_osi_version": "1.0.0", "layers": layers_yaml}, indent=2)

    @staticmethod
    def dependency_graph() -> dict:
        """Return dependency graph: which layer depends on which."""
        return {
            7: {"depends_on": [6], "provides": "compliance evidence"},
            6: {"depends_on": [5], "provides": "verification results"},
            5: {"depends_on": [4], "provides": "completed work"},
            4: {"depends_on": [3], "provides": "clean session state"},
            3: {"depends_on": [2], "provides": "target address + capabilities"},
            2: {"depends_on": [1], "provides": "authenticated channels"},
            1: {"depends_on": [], "provides": "running agent process"},
        }


# ── Demo ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    model = AgentOSIModel()
    print("=== Agent OSI Model v1.0.0 ===\n")

    # 1. Layer lookup
    print("1. Layer 4 (Session):")
    l4 = model.get_layer(4)
    print(f"   Name: {l4['name']}")
    print(f"   Responsibility: {l4['responsibility']}")
    print(f"   Status: {l4['status']}")
    print(f"   Examples: {l4['examples']}")

    # 2. Diagnose symptoms
    print("\n2. Diagnosing 'agent lost context after restart':")
    for match in model.diagnose("agent lost context after restart"):
        print(f"   → Layer {match['layer']} ({match['name']}): {match['responsibility']}")

    print("\n3. Diagnosing 'two agents overwrote same file':")
    for match in model.diagnose("two agents overwrote same file"):
        print(f"   → Layer {match['layer']} ({match['name']}): {match['responsibility']}")

    # 3. Infrastructure guidance
    print("\n4. Infrastructure for 'multi_agent' fleet:")
    for layer in model.infrastructure_guide("multi_agent"):
        print(f"   L{layer['layer']}: {layer['name']} — {layer['responsibility']}")

    # 4. Dependency graph
    print("\n5. Dependency chain (top-down):")
    for lid in range(7, 0, -1):
        deps = model.dependency_graph()[lid]
        dep_str = f"depends on L{deps['depends_on']}" if deps['depends_on'] else "no dependencies"
        print(f"   L{lid} ({LAYERS[lid]['name']}): {dep_str} → {deps['provides']}")

    # 5. Machine-readable export
    print("\n6. Machine-readable YAML (first 200 chars):")
    yaml_str = model.to_yaml()
    print(f"   {yaml_str[:200]}...")

    print("\n=== Complete ===")
```
