# AutoGen

**Version:** 0.4+
**Status:** Published
**Layer:** L5 — Coordination
**Steward:** Microsoft
**License:** MIT
**Repository:** https://github.com/microsoft/autogen
**Documentation:** https://microsoft.github.io/autogen/

## Relationship to WWA

AutoGen is a multi-agent conversation framework covering similar ground to WWA's Coordination Protocol (ACP). Both enable multiple agents to collaborate on tasks through structured communication. AutoGen uses an event-driven, pub-sub model where agents subscribe to topics and react to published messages — this maps to WWA's ECP pub-sub semantics. AutoGen's group chat manager orchestrates agent conversations, analogous to WWA's Coordinator role. The key difference: AutoGen is an SDK implementation with opinionated agent types (AssistantAgent, UserProxyAgent), while WWA defines protocol-level specifications that any implementation can follow.

## Architecture

AutoGen v0.4+ is built on an event-driven, asynchronous messaging core. Agents are actors that publish messages to topics and subscribe to topics they care about. A GroupChat manager routes messages between agents, managing turn-taking and conversation flow. Agents can execute code in sandboxed environments (Docker-based), call tools, and delegate to sub-agents. The framework supports both Python and .NET, with the newer architecture (v0.4) separating agent logic from communication patterns more cleanly than the original v0.2 design.

## Features

- Agent teams: assemble agents for collaborative task execution
- Group chat: managed multi-agent conversations with turn-taking
- Code execution: sandboxed Docker environments for agent-generated code
- Tool use: agents can invoke external functions and APIs
- Event-driven messaging: pub-sub communication between agents
- Python and .NET SDKs
- Large community (Microsoft-backed, 35k+ ★ on GitHub)

## Governance

Maintained by Microsoft Research under MIT license. As a Microsoft project, strategic direction is primarily set by Microsoft's AI research teams, with community contributions welcomed via GitHub. The project has a large and active open-source community. AutoGen v0.4 represents a significant architectural rework led by Microsoft in collaboration with academic and industry partners.

## Examples

Implementation examples for this version:

| Language | File |
|----------|------|
| Python | [related-autogen/v1.0.0/python.md](related-autogen/v1.0.0/python.md) |
| TypeScript | [related-autogen/v1.0.0/typescript.md](related-autogen/v1.0.0/typescript.md) |
