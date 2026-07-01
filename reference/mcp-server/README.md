# WWA MCP Server

MCP server wrapper that exposes the WWA Reference Agent as tools for any MCP-compatible client (Claude Code, Cursor, Codex, etc.).

## Tools

| Tool | Description |
|------|-------------|
| `wwa_check_health(agent_url)` | Check agent health, uptime, active handoffs, and protocol support |
| `wwa_query_capabilities(agent_url)` | Query the agent's capability manifest (YAML) |
| `wwa_send_handoff(agent_url, task, context)` | Send a task handoff request via IACP |

## Quick Start

```bash
# From the repository root:
pip install -e reference/mcp-server

# Run as an MCP stdio server:
wwa-mcp-server
```

Or point an MCP client directly at the script:

```bash
pip install mcp[cli] httpx
python reference/mcp-server/server.py
```

## Requirements

- Python 3.11+
- A running WWA Reference Agent (e.g. `docker compose up` from `reference/agent/`)

## License

CC BY 4.0
