"""
WWA MCP Server — expose the WWA Reference Agent as MCP tools.

MCP tools provided:
  - wwa_check_health(agent_url)         — check agent health and status
  - wwa_query_capabilities(agent_url)   — list agent capabilities
  - wwa_send_handoff(agent_url, task, context) — initiate a task handoff

Usage (one-liner):
    pip install mcp[cli] httpx
    python reference/mcp-server/server.py

Or from the pyproject.toml entry point:
    pip install -e reference/mcp-server
    wwa-mcp-server
"""
import json
import uuid
from datetime import datetime, timezone

import httpx

from mcp.server.fastmcp import FastMCP

server = FastMCP("wwa-mcp-server")


@server.tool()
async def wwa_check_health(agent_url: str) -> str:
    """Check the health and status of a running WWA reference agent.

    Returns agent identity, uptime, active handoffs, known peers,
    registry registration status, and supported protocols.
    """
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(f"{agent_url.rstrip('/')}/health")
        resp.raise_for_status()
        return json.dumps(resp.json(), indent=2)


@server.tool()
async def wwa_query_capabilities(agent_url: str) -> str:
    """Query the capability manifest (YAML) of a WWA reference agent.

    Returns the agent's declared capabilities, resources, endpoint,
    and identity information per the Capability Manifest v1.1.0 spec.
    """
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(f"{agent_url.rstrip('/')}/manifest.yaml")
        resp.raise_for_status()
        return resp.text


@server.tool()
async def wwa_send_handoff(agent_url: str, task: str, context: str = "{}") -> str:
    """Send a task handoff request to a WWA reference agent via IACP.

    task:      Description of the task to hand off.
    context:   Optional JSON object with additional context (workspace info,
               constraints, quality checklist, etc.). Defaults to empty object.
    """
    context_data = json.loads(context)

    handoff_id = str(uuid.uuid4())
    envelope = {
        "version": "1.0",
        "message_id": str(uuid.uuid4()),
        "correlation_id": None,
        "sender": {"agent_id": "mcp-client"},
        "recipient": {"agent_id": "wwa-reference"},
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "ttl_seconds": 3600,
        "message": {
            "type": "request",
            "intent": "handoff",
            "payload": {
                "handoff_id": handoff_id,
                "task_id": str(uuid.uuid4()),
                "sender": {"agent_id": "mcp-client"},
                "context": {
                    "task_description": task,
                    "workspace_path": context_data.get("workspace_path", ""),
                    "state_snapshot": context_data.get("state_snapshot", {}),
                    "agent_memory": context_data.get("agent_memory", {}),
                    "tools_required": context_data.get("tools_required", []),
                    "constraints": context_data.get("constraints", {}),
                },
                "quality_checklist": context_data.get("quality_checklist", []),
            },
        },
    }

    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.post(
            f"{agent_url.rstrip('/')}/iacp/message",
            json=envelope,
        )
        resp.raise_for_status()
        return json.dumps(resp.json(), indent=2)


def main():
    server.run()


if __name__ == "__main__":
    main()
