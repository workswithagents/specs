# Agent Asynchronous Messaging Protocol (AAMP)

**Version:** 1.1
**Status:** Published
**Layer:** L4/L5 — Session / Coordination
**Steward:** ByteDance / Lark
**License:** MIT
**Repository:** https://github.com/larksuite/aamp
**Specification:** https://github.com/larksuite/aamp

## Relationship to WWA

AAMP is complementary to WWA's ECP (Ephemeral Communication Protocol). WWA's ECP covers synchronous, ephemeral agent communication over WebSocket or IPC channels. AAMP covers asynchronous, mailbox-based dispatch over SMTP/JMAP — agents receive tasks as email-like messages and respond when ready. AAMP adds persistent addressing and store-and-forward semantics that WWA's ECP doesn't natively provide. The two could be layered: ECP for real-time coordination within a collaboration session, AAMP for cross-organizational, async task dispatch.

### Problem

There is no standard mechanism for asynchronous message delivery between agents. Existing protocols assume both agents are online simultaneously, requiring polling loops, retry logic, and custom queuing infrastructure. Without a mailbox abstraction, agents cannot send tasks and disconnect — every interaction must be a live, synchronous session, which breaks down for long-running work, offline agents, and cross-timezone collaboration.

### Solution

AAMP gives each agent a persistent mailbox address and defines structured task dispatch over standard email protocols (SMTP/JMAP). Agents send tasks as structured envelopes to addresses, and recipients process them when they come online — store-and-forward is built in, not bolted on. The protocol adds pairing codes for secure agent discovery, task cancellation, and help-needed escalation, bridging the gap between real-time agent protocols and human communication channels.

### When to use

- Cross-organizational task dispatch where agents may be offline or in different timezones
- Long-running agent tasks where the sender doesn't need to wait for completion
- Human-agent handoff over existing communication channels (email, messaging platforms)
- Store-and-forward patterns where message persistence and redelivery are critical

### When NOT to use

- Real-time synchronous agent communication — use IACP or ECP for low-latency, bidirectional messaging
- Ephemeral, single-session collaboration — the mailbox overhead is unnecessary when both agents are always online
- Simple fire-and-forget notifications — a lightweight pub-sub system (like ECP topics) is simpler

### How it compares to similar specs

| Instead of THIS spec | When | Because |
|---|---|---|
| WWA IACP | Real-time bidirectional messaging within a session | IACP provides lower latency and richer message semantics for live collaboration |
| WWA ECP | Ephemeral pub-sub within a single session | ECP is simpler and doesn't require SMTP infrastructure or mailbox management |
| A2A | Task transfer with streaming progress updates | A2A uses HTTP/JSON-RPC with SSE for progress, better for interactive task tracking |

### What you lose without THIS spec

- No standard async message delivery — every project builds its own queue-and-poll mechanism
- Agents must be online simultaneously to communicate, breaking cross-timezone and long-running workflows
- No persistent addressing for agents — each system invents its own naming and routing
- No bridge to existing messaging infrastructure (email, Feishu, WeChat) for human-agent handoff

## Architecture

AAMP treats each agent as a mail recipient with a unique address. Tasks are dispatched as structured messages (task envelope) over SMTP or JMAP transports. Agents poll their mailboxes, process tasks, and send responses back. The protocol supports pairing codes for secure agent discovery, cancellation of in-flight tasks, and help-needed escalation. Bridge adapters connect AAMP to existing messaging platforms (Feishu, WeChat), enabling human-agent handoff over familiar channels. An OpenClaw plugin provides integration with broader agent frameworks.

## Features

- `task.dispatch`: send structured tasks to agent addresses over SMTP/JMAP
- `task.cancel`: cancel in-flight tasks by reference
- `task.help_needed`: escalate tasks requiring human intervention
- Pairing codes for secure agent-to-agent discovery
- Bridge adapters for Feishu and WeChat
- OpenClaw plugin for framework integration
- Node.js SDK, Python SDK, and CLI tooling
- 88 ★ on GitHub

## Governance

Created and maintained by ByteDance/Lark under MIT license. The project is open-source on GitHub. As a single-vendor project, direction and governance are primarily driven by ByteDance's Lark team, with community contributions welcomed.

## Examples

### Node.js SDK
```javascript
import { AAMPClient } from '@larksuite/aamp';

const client = new AAMPClient({
  transport: 'smtp',
  address: 'agent-prod@example.com',
  mailbox: 'imaps://mail.example.com',
});

// Dispatch a task to another agent
await client.dispatch({
  to: 'builder-agent@example.com',
  task: {
    id: 'task-001',
    description: 'Run integration tests for v2.1',
    priority: 'high',
    deadline: '2026-06-22T00:00:00Z',
  },
});

// Cancel a task
await client.cancel({ taskId: 'task-001' });

// Request human help
await client.helpNeeded({
  taskId: 'task-001',
  reason: 'Unexpected test failure in auth module',
  escalation: ['human-ops@example.com'],
});
```

### Python SDK
```python
from aamp import AAMPClient

client = AAMPClient(
    transport="smtp",
    address="agent-prod@example.com",
    mailbox="imaps://mail.example.com",
)

client.dispatch(
    to="builder-agent@example.com",
    task={
        "id": "task-001",
        "description": "Run integration tests for v2.1",
        "priority": "high",
    }
)
```

### CLI
```bash
aamp dispatch \
  --to builder-agent@example.com \
  --task '{"id":"task-001","description":"Run integration tests"}' \
  --priority high
```
