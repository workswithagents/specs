# Agent OSI Model — TypeScript Example

Complete TypeScript implementation for the Agent OSI Model (v1.0.0).

```typescript
/**
 * Agent OSI Model v1.0.0 — TypeScript Reference Implementation
 *
 * Utilities for the 7-layer agent infrastructure model:
 *   - Layer definitions and lookup
 *   - Symptom diagnosis (symptom → layer)
 *   - Infrastructure scope guidance
 *   - Dependency graph
 */

interface LayerDef {
  name: string;
  responsibility: string;
  interfaceUp: string;
  examples: string;
  debug: string[];
  status: string;
}

const LAYERS: Record<number, LayerDef> = {
  1: {
    name: "Execution",
    responsibility: "Hardware, model runtime, tool execution",
    interfaceUp: "Provides running agent process",
    examples: "Blueprint Registry, model config, tool sandbox",
    debug: ["agent won't start", "model crash", "out of memory"],
    status: "live",
  },
  2: {
    name: "Communication",
    responsibility: "Agent messaging, authentication, API contracts",
    interfaceUp: "Provides authenticated channels",
    examples: "MCP, A2A, OpenAPI 3.1, Credential Proxy",
    debug: ["agent can't authenticate", "API call fails", "TLS error"],
    status: "live",
  },
  3: {
    name: "Discovery",
    responsibility: "Agent registry, capability advertisement, service location",
    interfaceUp: "Provides target agent address and capabilities",
    examples: "llms.txt, Capability Manifest, Agent Registry",
    debug: ["agent can't find service", "unknown capability", "peer not found"],
    status: "partial",
  },
  4: {
    name: "Session",
    responsibility: "State transfer, context preservation, handoff between sessions",
    interfaceUp: "Provides clean session state",
    examples: "Handoff Protocol, Context Packer",
    debug: ["agent lost context after restart", "handoff failed", "state corruption"],
    status: "in_proposal",
  },
  5: {
    name: "Coordination",
    responsibility: "Work distribution, consensus, conflict resolution, leader election",
    interfaceUp: "Provides completed work",
    examples: "Coordination Protocol, Cron Guard",
    debug: ["two agents overwrote same file", "race condition", "dead agent"],
    status: "spec_written",
  },
  6: {
    name: "Verification",
    responsibility: "Testing, evaluation, quality gates, regression detection",
    interfaceUp: "Provides verification results",
    examples: "Agent Test Suite, Pitfall Registry, Quality Gates",
    debug: ["agent produces wrong output", "regression", "test failure"],
    status: "partial",
  },
  7: {
    name: "Governance",
    responsibility: "Audit, compliance, sign-off, regulatory alignment",
    interfaceUp: "Provides compliance evidence",
    examples: "Regulated Handoff, Compliance-as-Code, Audit Trail",
    debug: ["compliance blocked deployment", "audit failure", "missing sign-off"],
    status: "planned",
  },
};

class AgentOSIModel {
  static getLayer(layerId: number): LayerDef | null {
    return LAYERS[layerId] ?? null;
  }

  static diagnose(symptom: string): { layer: number; name: string; responsibility: string }[] {
    const lower = symptom.toLowerCase();
    const matches: { layer: number; name: string; responsibility: string }[] = [];
    for (const [idStr, layer] of Object.entries(LAYERS)) {
      const id = parseInt(idStr);
      if (layer.debug.some(kw => lower.includes(kw.toLowerCase()))) {
        matches.push({ layer: id, name: layer.name, responsibility: layer.responsibility });
      }
    }
    return matches;
  }

  static infrastructureGuide(
    scope: "local" | "multi_agent" | "enterprise" | "regulated"
  ): { layer: number; name: string; responsibility: string }[] {
    const scopeMap: Record<string, number[]> = {
      local: [1, 2, 4],
      multi_agent: [1, 2, 3, 4, 5],
      enterprise: [1, 2, 3, 4, 5, 6, 7],
      regulated: [1, 2, 3, 4, 5, 6, 7],
    };
    const ids = scopeMap[scope] ?? [1, 2, 4];
    return ids.map(id => ({
      layer: id,
      name: LAYERS[id].name,
      responsibility: LAYERS[id].responsibility,
    }));
  }

  static toJSON(): object {
    return {
      agent_osi_version: "1.0.0",
      layers: Object.entries(LAYERS).map(([idStr, l]) => ({
        id: parseInt(idStr),
        name: l.name,
        responsibility: l.responsibility,
        interface_up: l.interfaceUp,
        infrastructure: l.examples.split(", "),
        status: l.status,
      })),
    };
  }

  static dependencyGraph(): Record<number, { dependsOn: number[]; provides: string }> {
    return {
      7: { dependsOn: [6], provides: "compliance evidence" },
      6: { dependsOn: [5], provides: "verification results" },
      5: { dependsOn: [4], provides: "completed work" },
      4: { dependsOn: [3], provides: "clean session state" },
      3: { dependsOn: [2], provides: "target address + capabilities" },
      2: { dependsOn: [1], provides: "authenticated channels" },
      1: { dependsOn: [], provides: "running agent process" },
    };
  }
}

// ── Demo ─────────────────────────────────────────────────────────

console.log("=== Agent OSI Model v1.0.0 ===\n");

// 1. Layer lookup
const l4 = AgentOSIModel.getLayer(4)!;
console.log("1. Layer 4 (Session):");
console.log(`   Name: ${l4.name}`);
console.log(`   Responsibility: ${l4.responsibility}`);
console.log(`   Status: ${l4.status}`);

// 2. Diagnose
console.log("\n2. Diagnosing 'agent lost context after restart':");
for (const m of AgentOSIModel.diagnose("agent lost context after restart")) {
  console.log(`   → Layer ${m.layer} (${m.name}): ${m.responsibility}`);
}

console.log("\n3. Diagnosing 'compliance blocked deployment':");
for (const m of AgentOSIModel.diagnose("compliance blocked deployment")) {
  console.log(`   → Layer ${m.layer} (${m.name}): ${m.responsibility}`);
}

// 3. Infrastructure guide
console.log("\n4. Infrastructure for 'regulated' scope:");
for (const l of AgentOSIModel.infrastructureGuide("regulated")) {
  console.log(`   L${l.layer}: ${l.name} — ${l.responsibility}`);
}

// 4. Dependency graph
console.log("\n5. Dependency chain (top-down):");
const deps = AgentOSIModel.dependencyGraph();
for (let lid = 7; lid >= 1; lid--) {
  const d = deps[lid];
  const depStr = d.dependsOn.length ? `depends on L${d.dependsOn}` : "no dependencies";
  console.log(`   L${lid} (${LAYERS[lid].name}): ${depStr} → ${d.provides}`);
}

// 5. JSON export
console.log("\n6. Machine-readable JSON (first 200 chars):");
const json = JSON.stringify(AgentOSIModel.toJSON());
console.log(`   ${json.slice(0, 200)}...`);

console.log("\n=== Complete ===");
```
