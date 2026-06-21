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
