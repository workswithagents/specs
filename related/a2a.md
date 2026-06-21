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
