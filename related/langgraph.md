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

Implementation examples for this version:

| Language | File |
|----------|------|
| Python | [related-langgraph/v1.0.0/python.md](related-langgraph/v1.0.0/python.md) |
| TypeScript | [related-langgraph/v1.0.0/typescript.md](related-langgraph/v1.0.0/typescript.md) |
