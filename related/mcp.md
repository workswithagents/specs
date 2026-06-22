# Model Context Protocol (MCP)

**Version:** 2025-11-25
**Status:** Published
**Layer:** L1 — Execution / Tool Integration
**Steward:** Anthropic / LF Projects
**License:** MIT
**Repository:** https://github.com/modelcontextprotocol/specification
**Specification:** https://modelcontextprotocol.io/specification/2025-11-25

## Relationship to WWA

MCP is complementary to WWA specs. MCP defines a wire protocol for agent-to-tool communication (tool discovery, invocation, resource access), while ASFS defines how skills are packaged and distributed. A WWA agent can use MCP as its tool-calling transport while following WWA's identity, handoff, and attestation protocols. MCP handles execution-layer concerns; WWA adds session, coordination, and audit layers above it.

### Problem

Every LLM-to-tool integration is a custom build — developers write bespoke glue code to connect each model to each tool, with no standard way for a model to discover what tools are available or invoke them. This means switching from OpenAI to Anthropic requires rewriting all tool-calling logic, and tool authors must build separate integrations for every LLM provider. The lack of a standard protocol fragments the ecosystem and wastes engineering effort on plumbing instead of capabilities.

### Solution

MCP defines a standardized client-server protocol over JSON-RPC 2.0 for tool discovery and invocation. A host application creates clients that connect to servers, which advertise their tools, resources, and prompts at connection time. The model can then call `tools/list` to discover capabilities and `tools/call` to invoke them, regardless of which LLM provider is behind the host. Tool authors build one MCP server, and any MCP-compatible host can use it.

### When to use

- Connecting LLMs to external tools, APIs, and data sources in a provider-agnostic way
- Building tool servers that should work with multiple LLM hosts (Claude, ChatGPT, IDEs)
- Adding tool-calling to an agent that doesn't have a built-in mechanism
- Standardizing tool interfaces across an organization so any agent can use any tool

### When NOT to use

- Agent-to-agent communication — use IACP or A2A for agent-agent messaging, not agent-tool
- Packaging and distributing skills with metadata — use ASFS for skill packaging with manifests and versioning
- Agent-to-human communication — MCP is for LLM-tool interaction, not human interfaces
- Simple, single-provider setups where the provider's native function calling is sufficient

### How it compares to similar specs

| Instead of THIS spec | When | Because |
|---|---|---|
| WWA ASFS | Distributing skills as versioned packages with manifests | ASFS is for skill packaging and discovery at the file/registry level; MCP is for runtime tool invocation |
| WWA IACP | Agent-to-agent messaging with session semantics | IACP handles inter-agent communication; MCP handles agent-to-tool communication |
| OpenAI function calling | Single-provider, OpenAI-only deployments | Native function calling is simpler when you're committed to OpenAI and don't need cross-provider portability |

### What you lose without THIS spec

- No standard protocol for LLM tool discovery and invocation — every integration is custom
- Tool authors must build N integrations for N LLM providers instead of one MCP server
- No capability negotiation at connection time — tools can't dynamically advertise what they support
- No standard transport options (stdio, HTTP+SSE, streamable HTTP) for different deployment scenarios

## Architecture

MCP follows a client-server architecture built on JSON-RPC 2.0. A **host** application (e.g., an AI IDE) creates **clients** that connect to **servers** exposing tools, resources, and prompts. Servers advertise their capabilities at connection time; clients invoke tools via `tools/call`. Transport options include stdio (subprocess-based) and HTTP+SSE (network-based). The protocol is transport-agnostic, with a streaming HTTP transport added in recent versions.

## Features

- Tool discovery and invocation via `tools/list` and `tools/call`
- Resource access with URI-based `resources/read`
- Prompt templates exposed via `prompts/get`
- Sampling support (servers can request LLM completions from the host)
- Transport-agnostic: stdio, HTTP+SSE, streamable HTTP
- Capability negotiation at connection handshake
- 8.4k ★, 370 contributors on GitHub

## Governance

Originally created by Anthropic and contributed to the Linux Foundation (LF Projects) for community governance. The specification is open-source under MIT license. Development happens on GitHub with an open RFC process for protocol changes. Multiple vendors (Anthropic, OpenAI, Google, Microsoft) have announced support.

## Examples

### Python
```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    server_params = StdioServerParameters(
        command="python",
        args=["my_mcp_server.py"]
    )
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            result = await session.call_tool("search", {"query": "hello"})
            print(result)

asyncio.run(main())
```

### TypeScript
```typescript
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

const transport = new StdioClientTransport({
  command: "node",
  args: ["server.js"],
});

const client = new Client({
  name: "example-client",
  version: "1.0.0",
});

await client.connect(transport);
const tools = await client.listTools();
const result = await client.callTool({
  name: "search",
  arguments: { query: "hello" },
});
```
