# CrewAI

**Version:** latest
**Status:** Published
**Layer:** L5 — Coordination
**Steward:** CrewAI
**License:** MIT
**Repository:** https://github.com/joaomdmoura/crewAI
**Documentation:** https://docs.crewai.com/

## Relationship to WWA

CrewAI is a role-based multi-agent orchestration framework similar in spirit to WWA's Delegation Framework. Both define how agents with specialized roles collaborate on tasks. CrewAI uses opinionated abstractions — Crew (the team), Agent (role-based with goals and backstory), Task (a work unit with expected output) — while WWA's Delegation Framework is a protocol specification that defines message formats and delegation semantics without prescribing class hierarchies. CrewAI's process flows (sequential and hierarchical) correspond to WWA's ACP execution models. A CrewAI implementation could be made WWA-compliant by wrapping its agent communication in IACP messages.

### Problem

Multi-agent teams need clear role boundaries — who is responsible for what, in what order do tasks execute, and how do agents hand off work. Without a role-based model, agents either duplicate effort or miss tasks entirely, and there's no built-in mechanism to define "this agent owns design, that agent owns implementation." Ad-hoc agent coordination produces unpredictable results at scale.

### Solution

CrewAI assigns each agent a role, goal, and backstory that shapes its behavior, then organizes agents into crews with defined process flows. Tasks have explicit owners and expected outputs, so accountability is built into the structure. The framework supports sequential execution (do A, then B, then C) and hierarchical execution (a manager agent delegates to worker agents), giving teams a predictable orchestration model without requiring custom state machine code.

### When to use

- Role-based agent teams where each agent has a clearly defined specialty (architect, developer, reviewer)
- Sequential task pipelines where work flows through stages with clear handoff points
- Teams that map naturally to human organizational structures (manager → workers)
- Rapid prototyping of multi-agent workflows in Python

### When NOT to use

- Flat agent groups without clear role differentiation — use A2A or AutoGen for peer-to-peer conversation
- Single-agent systems — the crew/task/agent abstraction is unnecessary overhead
- Production systems requiring vendor-neutral protocol compliance — CrewAI is a Python SDK, not a spec (use WWA Delegation for protocol-level interop)
- Non-Python environments — CrewAI is Python-only; use WWA specs for cross-language agent coordination

### How it compares to similar specs

| Instead of THIS spec | When | Because |
|---|---|---|
| AutoGen | Conversational multi-agent collaboration with group chat | AutoGen's conversation model is better for open-ended discussion; CrewAI is better for defined role pipelines |
| WWA Delegation | Vendor-neutral delegation protocol needed across implementations | WWA Delegation defines message formats and semantics without language or framework lock-in |
| WWA ACP | Graph-based or event-driven coordination models | ACP provides more flexible execution patterns beyond sequential/hierarchical |

### What you lose without THIS spec

- No standard role-based abstraction — every project defines its own role/task/team model from scratch
- No built-in sequential and hierarchical process flows for agent teams
- No shared crew memory for context sharing between agents in a team
- Python-only ecosystem lock-in if you build directly on CrewAI abstractions

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

### Python
```python
from crewai import Agent, Task, Crew, Process

# Define agents with roles
code_agent = Agent(
    role="Senior Python Developer",
    goal="Write clean, tested, production-ready Python code",
    backstory="You are a developer with 15 years of experience.",
    allow_code_execution=True,
)

review_agent = Agent(
    role="Code Reviewer",
    goal="Review code for bugs, security issues, and style violations",
    backstory="You catch issues others miss.",
)

architect_agent = Agent(
    role="Software Architect",
    goal="Design system architecture and delegate implementation",
    backstory="You design scalable systems.",
    allow_delegation=True,
)

# Define tasks
design_task = Task(
    description="Design a REST API for a task management system",
    expected_output="Architecture diagram and API specification",
    agent=architect_agent,
)

code_task = Task(
    description="Implement the REST API per the architecture design",
    expected_output="Working FastAPI application with tests",
    agent=code_agent,
)

review_task = Task(
    description="Review the implemented API code",
    expected_output="Review report with findings",
    agent=review_agent,
)

# Assemble the crew in hierarchical mode
crew = Crew(
    agents=[architect_agent, code_agent, review_agent],
    tasks=[design_task, code_task, review_task],
    process=Process.hierarchical,
    verbose=True,
)

result = crew.kickoff()
print(result)
```
