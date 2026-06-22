# OpenAI Agents SDK

**Version:** latest
**Status:** Published
**Layer:** L5 — Orchestration
**Steward:** OpenAI
**License:** MIT (SDK only — models proprietary)
**Repository:** https://github.com/openai/openai-agents-python
**Documentation:** https://openai.github.io/openai-agents-python/

## Relationship to WWA

The OpenAI Agents SDK is an SDK-level implementation, not a specification. It implements orchestration patterns similar to WWA's IACP and Delegation Framework but in an OpenAI-specific, opinionated way. Handoffs between agents in the OpenAI SDK use a proprietary `Agent` class with built-in handoff targets, whereas WWA defines spec-level, vendor-neutral protocols (IACP for messaging, Handoff Protocol for task transfer). The SDK recently added MCP integration, showing convergence toward open tool-calling standards that WWA also builds upon. Developers using WWA specs could implement their protocols on top of the OpenAI Agents SDK as a runtime.

### Problem

Building production agent systems on OpenAI models requires managing conversation loops, tool call processing, handoff routing, guardrails, and tracing — infrastructure that every developer rebuilds from scratch. Without a managed agent runtime, developers spend more time on plumbing (did the tool call succeed? where does the handoff go? was this output safe?) than on agent capabilities. Raw API calls don't provide the execution loop, observability, or safety checks that production agents need.

### Solution

The OpenAI Agents SDK provides a managed agent runtime centered on the `Agent` class — a configured LLM with instructions, tools, guardrails, and handoff targets. The `Runner` executes agents in a loop, automatically processing tool calls and handoffs until a final output is produced. Built-in guardrails validate inputs and outputs at each step, and OpenTelemetry tracing provides observability without custom instrumentation. Handoffs between specialized agents are declarative, not imperative — you define targets, and the SDK routes conversations automatically.

### When to use

- Building production agent systems on OpenAI models (GPT-4o, o-series)
- Rapid prototyping of multi-agent systems with handoffs and guardrails
- Projects where built-in OpenTelemetry tracing reduces observability engineering effort
- Teams already committed to the OpenAI ecosystem (API, models, platform)

### When NOT to use

- Non-OpenAI models — the SDK requires OpenAI API keys and is tightly coupled to OpenAI's model interface
- Platform-agnostic agent deployments — use WWA specs or framework-agnostic SDKs if you need model portability
- Vendor-neutral protocol compliance requirements — the OpenAI Agents SDK is a single-vendor implementation, not a spec
- Systems requiring cross-framework agent handoff — use A2A or WWA Handoff for framework-agnostic task transfer

### How it compares to similar specs

| Instead of THIS spec | When | Because |
|---|---|---|
| WWA IACP + WWA SDK | Vendor-neutral agent messaging and handoff across model providers | WWA specs define protocols any runtime can implement; OpenAI SDK is tied to OpenAI models |
| AutoGen | Multi-agent conversation with group chat and code execution | AutoGen is Microsoft-backed with .NET/Python support; OpenAI SDK is simpler but OpenAI-only |
| LangGraph | Graph-based workflows with human-in-the-loop and checkpointing | LangGraph provides finer control over state and execution; OpenAI SDK focuses on simplicity |

### What you lose without THIS spec

- No managed agent runtime for OpenAI models — every project builds its own conversation loop, tool processing, and handoff routing
- No built-in guardrails for input/output validation at each agent step
- No declarative agent handoff — routing between specialized agents must be implemented manually
- OpenTelemetry tracing must be wired up from scratch for each agent deployment

## Architecture

The SDK centers around the `Agent` class — a configured LLM with instructions, tools, guardrails, and handoff targets. The `Runner` executes agents in a loop, processing tool calls and handoffs automatically until a final output is produced. Guardrails are check-functions that run before and after each agent step. Tracing is built-in, with OpenTelemetry export. Sandbox agents provide isolated execution environments. The SDK is Python-only, with model access requiring OpenAI API keys.

## Features

- Agents: configured LLMs with instructions, tools, and handoff targets
- Handoffs: seamless transfer between agents (similar to WWA L4 Handoff)
- Guardrails: input/output validation at each agent step
- Tracing: built-in OpenTelemetry-integrated observability
- Sandbox agents: isolated execution for untrusted code
- MCP integration: connect agents to MCP servers for tool calling
- Python-only SDK

## Governance

Created and maintained by OpenAI. The SDK itself is MIT-licensed and open-source, but the underlying models are proprietary and require an OpenAI API key. Governance is entirely single-vendor — OpenAI controls the roadmap, API design, and release cadence. Community contributions are accepted via GitHub pull requests but direction is set by OpenAI's agent team.

## Examples

### Python (Agent + Runner + Handoff)
```python
from agents import Agent, Runner, handoff

# Define specialized agents
code_agent = Agent(
    name="Code Agent",
    instructions="You write and review code.",
    model="gpt-4o",
    tools=[terminal_tool, file_tool],
)

review_agent = Agent(
    name="Review Agent",
    instructions="You review code for quality and security.",
    model="gpt-4o",
)

# Orchestrator agent with handoff targets
orchestrator = Agent(
    name="Orchestrator",
    instructions="You coordinate coding tasks.",
    handoffs=[
        handoff(code_agent, on_handoff="Sending to code agent..."),
        handoff(review_agent, on_handoff="Sending for review..."),
    ],
)

# Run the orchestrator
result = await Runner.run(
    orchestrator,
    input="Write a function to sort a list and get it reviewed.",
)
print(result.final_output)
```
