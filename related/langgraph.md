# LangGraph

**Version:** latest
**Status:** Published
**Layer:** L5 — Orchestration
**Steward:** LangChain
**License:** MIT (SDK) / proprietary (LangSmith platform)
**Website:** https://www.langchain.com/langgraph
**Repository:** https://github.com/langchain-ai/langgraph

## Relationship to WWA

LangGraph is an orchestration framework that implements patterns similar to WWA's ACP (Agent Coordination Protocol). Both model agent workflows as graphs with nodes, edges, and state management. LangGraph adds human-in-the-loop interrupts — points where agent execution pauses for human approval — which corresponds to WWA's Clarification Protocol pattern. LangGraph's persistence layer (checkpoints) provides state recovery similar to WWA's IACP Fault Tolerance. As a Python/TypeScript SDK rather than a spec, LangGraph is an implementation vehicle; WWA specs could be realized as LangGraph state machines.

### Problem

Real-world agent workflows are rarely linear — they need conditional branching ("if the code compiles, proceed to review; otherwise, loop back to fix"), loops, human approval gates, and state persistence across steps. Building this from scratch means managing state dictionaries, implementing checkpoint/restore, and wiring up interrupt signals — all infrastructure code that has nothing to do with the agent's actual task. Without a graph-based framework, complex workflows collapse into brittle if/else chains.

### Solution

LangGraph models agent workflows as directed graphs where nodes are computation steps and edges are transitions (conditional or unconditional). State flows through the graph as a typed dictionary, checkpointed at every step for persistence, replay, and debugging. Human-in-the-loop interrupts pause execution at specified nodes, waiting for approval before continuing — no custom signaling infrastructure required. Sub-graphs allow composing complex agents from simpler, tested components.

### When to use

- Complex agent workflows with conditional branching, cycles, and retry loops
- Systems requiring human approval gates at critical decision points
- Debugging-heavy development where checkpoint replay and time-travel debugging are valuable
- LangChain ecosystem projects where LangSmith tracing and deployment are part of the stack

### When NOT to use

- Simple linear pipelines (do A, then B, then C) — use WWA Handoff or a sequential script
- Single-agent systems with no branching — a single LLM call loop is simpler
- Vendor-neutral protocol requirements — LangGraph is a LangChain-specific SDK, not an interoperable spec
- Production systems needing framework-agnostic state machine definitions (use WWA ACP for protocol-level graphs)

### How it compares to similar specs

| Instead of THIS spec | When | Because |
|---|---|---|
| WWA ACP | Protocol-level workflow definitions across implementations | ACP defines graph semantics without SDK lock-in, enabling any runtime to execute the same workflow |
| CrewAI | Role-based agent teams with clear owner-task mapping | CrewAI's role/goal/backstory model is simpler for team orchestration without custom graph logic |
| AutoGen | Conversational multi-agent collaboration with group chat | AutoGen's pub-sub model is better for open-ended agent conversations than for structured state machines |

### What you lose without THIS spec

- No standard graph-based workflow framework with built-in state persistence and replay
- Every project builds its own checkpoint/restore, interrupt signaling, and conditional routing infrastructure
- No built-in human-in-the-loop pattern — each system invents its own approval gate mechanism
- LangChain ecosystem lock-in if you adopt LangGraph as your orchestration layer

## Architecture

LangGraph models agent workflows as directed graphs where nodes are computation steps (LLM calls, tool invocations, sub-agents) and edges are transitions (unconditional or conditional). State flows through the graph as a typed dictionary. Checkpoints capture state at every step, enabling persistence, replay, and time travel debugging. Human-in-the-loop interrupts pause execution at specified nodes, waiting for approval or input before continuing. Streaming emits tokens and state updates in real-time. The framework supports both Python and TypeScript.

## Features

- State graphs: nodes (computation), edges (transitions), typed state dictionaries
- Human-in-the-loop: interrupt execution for approval or input
- Persistence: checkpoint state at every step for replay and debugging
- Streaming: real-time token and state emissions
- Conditional edges: dynamic routing based on state
- Sub-graphs: compose graphs within graphs for modular agents
- Python and TypeScript SDKs

## Governance

Maintained by LangChain (the company). The LangGraph SDK is MIT-licensed and open-source. The LangSmith platform (tracing, evaluation, deployment) is proprietary. Governance is single-vendor — LangChain controls the roadmap. Community contributions are accepted but strategic direction comes from the company. LangGraph has a large user community due to LangChain's established ecosystem.

## Examples

### Python
```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Literal

class AgentState(TypedDict):
    messages: list
    next_agent: str
    final_output: str

# Define agent nodes
def code_agent(state: AgentState) -> AgentState:
    response = llm.invoke(state["messages"])
    return {"messages": state["messages"] + [response]}

def review_agent(state: AgentState) -> AgentState:
    response = llm.invoke(state["messages"])
    return {"messages": state["messages"] + [response], "final_output": response}

# Build the graph
graph = StateGraph(AgentState)
graph.add_node("code", code_agent)
graph.add_node("review", review_agent)
graph.add_node("human_approval", human_interrupt)

graph.set_entry_point("code")
graph.add_edge("code", "human_approval")

# Conditional: only proceed to review if approved
def approval_router(state: AgentState) -> Literal["review", "code"]:
    if state.get("approved"):
        return "review"
    return "code"

graph.add_conditional_edges("human_approval", approval_router)
graph.add_edge("review", END)

app = graph.compile()
result = app.invoke({"messages": ["Write a quicksort implementation"]})
```
