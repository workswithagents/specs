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
