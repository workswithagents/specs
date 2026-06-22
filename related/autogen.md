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

### Problem

Multi-agent conversations quickly devolve into chaos without structure — agents talk over each other, messages loop endlessly, and there's no clear mechanism for who speaks when or how results converge. Building turn-taking, message routing, and conversation state management from scratch for every multi-agent system is error-prone and creates incompatible ad-hoc solutions.

### Solution

AutoGen provides a managed conversation framework where agents communicate through an event-driven pub-sub model. A GroupChat manager orchestrates turn-taking — agents publish messages to topics and subscribe to topics they care about, and the manager routes messages to keep conversations productive. Agents can execute code in sandboxed Docker environments and delegate to sub-agents, making the framework suitable for complex collaborative coding and problem-solving workflows.

### When to use

- Conversational multi-agent systems where agents need to discuss, debate, and iterate
- Group chat patterns where multiple agents contribute to a shared problem-solving session
- Code generation and review workflows with sandboxed execution
- Microsoft ecosystem projects where .NET/Python and Azure integration are valuable

### When NOT to use

- Simple sequential pipelines — use WWA Handoff or a linear workflow for straightforward task chains
- Single-agent systems — the group chat overhead is wasted when one agent can handle the task
- Cross-framework agent teams — AutoGen requires agents to be built within its framework (use A2A or WWA for framework-agnostic handoff)
- Production deployments requiring vendor-neutral protocol compliance — AutoGen is an SDK, not a spec

### How it compares to similar specs

| Instead of THIS spec | When | Because |
|---|---|---|
| CrewAI | Role-based task pipelines with clear owner-task assignments | CrewAI's role/goal/backstory model provides clearer accountability for structured workflows |
| WWA ACP | Vendor-neutral coordination protocol needed across implementations | ACP defines protocol semantics without locking into a specific SDK or language |
| LangGraph | Graph-based workflows with human-in-the-loop and conditional branching | LangGraph offers finer control over state transitions and interrupt points |

### What you lose without THIS spec

- No standard framework for managing multi-agent conversations with turn-taking and routing
- Every project builds its own ad-hoc group chat logic, creating incompatibility between agent teams
- No built-in sandboxed code execution for agent-generated code
- Microsoft-backed ecosystem with dedicated research and support guarantees

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

### Python
```python
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

model_client = OpenAIChatCompletionClient(model="gpt-4o")

# Define agents
code_agent = AssistantAgent(
    name="code_agent",
    model_client=model_client,
    system_message="You write Python code. Output code blocks.",
)

reviewer_agent = AssistantAgent(
    name="reviewer_agent",
    model_client=model_client,
    system_message="You review code and suggest improvements.",
)

# Create a team with round-robin coordination
team = RoundRobinGroupChat(
    [code_agent, reviewer_agent],
    max_turns=6,
)

# Run the team
async def main():
    result = await Console(
        team.run_stream(task="Write a function to merge two sorted lists")
    )
    print(f"Final result: {result.messages[-1].content}")

# import asyncio; asyncio.run(main())
```
