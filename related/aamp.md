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

Implementation examples for this version:

| Language | File |
|----------|------|
| Python | [related-aamp/v1.0.0/python.md](related-aamp/v1.0.0/python.md) |
| TypeScript | [related-aamp/v1.0.0/typescript.md](related-aamp/v1.0.0/typescript.md) |
| CLI | [related-aamp/v1.0.0/bash.md](related-aamp/v1.0.0/bash.md) |
| Node.js SDK | [related-aamp/v1.0.0/javascript.md](related-aamp/v1.0.0/javascript.md) |
