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
