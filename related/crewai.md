# CrewAI

**Version:** 1.9.3
**Status:** Published
**Layer:** L5 — Coordination
**Steward:** CrewAI
**License:** MIT
**Repository:** https://github.com/joaomdmoura/crewAI
**Documentation:** https://docs.crewai.com/

## Relationship to WWA

CrewAI is a role-based multi-agent orchestration framework similar in spirit to WWA's Delegation Framework. Both define how agents with specialized roles collaborate on tasks. CrewAI uses opinionated abstractions — Crew (the team), Agent (role-based with goals and backstory), Task (a work unit with expected output) — while WWA's Delegation Framework is a protocol specification that defines message formats and delegation semantics without prescribing class hierarchies. CrewAI's process flows (sequential and hierarchical) correspond to WWA's ACP execution models. A CrewAI implementation could be made WWA-compliant by wrapping its agent communication in IACP messages.

## Architecture

CrewAI organizes agents in a **Crew** — a team of agents that collaborate to complete a set of tasks. Each **Agent** has a role, goal, and backstory that shapes its behavior. Tasks have descriptions, expected outputs, and can specify which agent should execute them. The crew runs tasks in either **sequential** mode (one after another) or **hierarchical** mode (a manager agent delegates tasks to worker agents). Agents can use tools (including MCP servers) and share context through the crew's shared memory. The framework is Python-only.

## Features

- Role-based agents: each agent has a defined role, goal, and backstory
- Tasks: work units with descriptions, expected outputs, and agent assignment
- Crews: teams of agents with defined process flows
- Sequential and hierarchical process modes
- Tool integration including MCP server support
- Shared crew memory for context sharing
- Python-only SDK

## Governance

Maintained by CrewAI (the company) under MIT license. The open-source framework is community-facing, with the company offering a hosted platform (CrewAI Enterprise) for production deployments. Governance is single-vendor, with CrewAI setting the roadmap. The project has a large community with 25k+ ★ on GitHub.

## Examples

Implementation examples for this version:

| Language | File |
|----------|------|
| Python | [related-crewai/v1.0.0/python.md](related-crewai/v1.0.0/python.md) |
| TypeScript | [related-crewai/v1.0.0/typescript.md](related-crewai/v1.0.0/typescript.md) |
