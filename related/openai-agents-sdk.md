# OpenAI Agents SDK

**Version:** 0.17.6
**Status:** Published
**Layer:** L5 — Orchestration
**Steward:** OpenAI
**License:** MIT (SDK only — models proprietary)
**Repository:** https://github.com/openai/openai-agents-python
**Documentation:** https://openai.github.io/openai-agents-python/

## Relationship to WWA

The OpenAI Agents SDK is an SDK-level implementation, not a specification. It implements orchestration patterns similar to WWA's IACP and Delegation Framework but in an OpenAI-specific, opinionated way. Handoffs between agents in the OpenAI SDK use a proprietary `Agent` class with built-in handoff targets, whereas WWA defines spec-level, vendor-neutral protocols (IACP for messaging, Handoff Protocol for task transfer). The SDK recently added MCP integration, showing convergence toward open tool-calling standards that WWA also builds upon. Developers using WWA specs could implement their protocols on top of the OpenAI Agents SDK as a runtime.

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

Implementation examples for this version:

| Language | File |
|----------|------|
| Python | [related-openai-agents-sdk/v1.0.0/python.md](related-openai-agents-sdk/v1.0.0/python.md) |
| TypeScript | [related-openai-agents-sdk/v1.0.0/typescript.md](related-openai-agents-sdk/v1.0.0/typescript.md) |
