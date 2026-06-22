# Agent-to-Agent Protocol (A2A)

**Version:** 1.0 (2025)
**Status:** Published
**Layer:** L4 — Session / Handoff
**Steward:** Google
**License:** Apache 2.0
**Repository:** https://github.com/a2aproject/A2A
**Specification:** https://github.com/a2aproject/A2A

## Relationship to WWA

A2A overlaps with WWA Handoff Protocol — both define mechanisms for one agent to transfer work to another. A2A uses an agent card system (identity + capabilities advertised as JSON cards) and JSON-RPC task lifecycle management. WWA Handoff uses `state_context_hash`, Ed25519 identity signatures, and a quality checklist. Both are transport-agnostic, but A2A is more opinionated about the card-exchange discovery pattern, while WWA layers discovery into the Agent Registry (L3).

### Problem

Agents built on different frameworks (LangChain, AutoGen, CrewAI, custom) cannot hand off tasks to each other without bespoke adapter code. Each framework invents its own handoff mechanism, creating silos that force organizations to standardize on a single agent stack. There is no common language for one agent to say "I need help — here's the context, take over."

### Solution

A2A provides a vendor-neutral protocol for cross-framework agent task transfer. Every agent advertises an Agent Card — a machine-readable JSON document describing its identity, capabilities, and endpoint — so other agents can discover and invoke it via JSON-RPC. Tasks follow a standard lifecycle (submitted → working → completed/failed/canceled) with optional streaming updates, giving callers visibility into progress without polling.

### When to use

- Cross-framework agent collaboration where agents are built on different stacks
- Multi-vendor agent ecosystems where no single party controls all agents
- Public-facing agent endpoints that third parties can discover and invoke
- Long-running task delegation with progress streaming requirements

### When NOT to use

- All agents in the ecosystem are built on the same framework — use that framework's native handoff instead
- Single-organization deployment with a central orchestrator — use WWA Handoff for simpler identity-based transfer
- Real-time, low-latency agent coordination — A2A's HTTP/JSON-RPC transport adds overhead versus direct messaging (use IACP)

### How it compares to similar specs

| Instead of THIS spec | When | Because |
|---|---|---|
| WWA Handoff | Single-org, Ed25519 identity already deployed | WWA Handoff is simpler and ties into WWA's attestation and registry layers |
| IACP | Real-time agent-to-agent messaging within a session | IACP provides lower-latency, bidirectional messaging versus A2A's task-submission model |
| OpenAI Agents SDK handoff | All agents use OpenAI models in a single codebase | Native handoff is simpler and doesn't require exposing Agent Cards over HTTP |

### What you lose without THIS spec

- No standard way for agents from different frameworks to discover and invoke each other
- Every cross-framework integration requires custom adapter code and point-to-point agreements
- No standard task lifecycle — each integration must reinvent status tracking, cancellation, and streaming
- Third-party agents cannot self-describe their capabilities in a machine-readable format

## Architecture

A2A uses a client-server model where each agent exposes an **Agent Card** — a JSON document describing its identity, capabilities, and endpoint. Agents discover each other by fetching cards, then invoke tasks via JSON-RPC 2.0 over HTTP. Tasks follow a lifecycle: submitted → working → completed/failed/canceled. Optional streaming updates are supported via server-sent events (SSE). Long-running tasks can be polled for status.

## Features

- Agent Card: identity, capabilities, skills, and endpoint metadata
- Task lifecycle management: submit, query status, cancel
- JSON-RPC 2.0 transport over HTTP
- Server-sent events for streaming task updates
- Multi-modal support (text, images, structured data)
- Multi-agent discovery via card exchange
- Open-source reference implementations in Python and TypeScript

## Governance

Created and maintained by Google under Apache 2.0 license. The project is open-source and accepts community contributions. As a Google-backed protocol, it benefits from dedicated engineering resources but remains a single-vendor stewarded project rather than a multi-stakeholder standards body.

## Examples

### Python
```python
from a2a.client import A2AClient
from a2a.types import TaskSendParams, Message, Part, Task

async def main():
    client = A2AClient("http://agent-b.example.com")

    # Send task to another agent
    task: Task = await client.send_task(
        TaskSendParams(
            message=Message(
                role="user",
                parts=[Part.from_text("Analyze this dataset")],
            )
        )
    )

    # Poll for status
    status = await client.get_task(task.id)
    print(f"Status: {status.state}")

    # Subscribe to streaming updates
    async for event in client.subscribe(task.id):
        print(f"Update: {event}")
```

### TypeScript
```typescript
import { A2AClient } from "@a2aproject/sdk";

const client = new A2AClient("http://agent-b.example.com");

const task = await client.sendTask({
  message: {
    role: "user",
    parts: [{ text: "Analyze this dataset" }],
  },
});

// Stream updates
for await (const event of client.subscribeToTask(task.id)) {
  console.log("Update:", event);
}
```
