# Capability Manifest — cURL Examples

## Register Agent
```bash
curl -X POST https://workswithagents.dev/v1/agents/register -H "Content-Type: application/json" -d '{"manifest_version":"1.0.0","agent_id":"hermes-spfx-builder","capabilities":[{"action":"build","target":"spfx","success_rate":0.94,"avg_duration_seconds":180}],"tools":["node","gulp","npm"],"endpoint":{"address":"agent://spfx-builder:8782","protocol":"acp"},"status":{"state":"healthy","load":0.0,"current_tasks":0,"max_tasks":3}}'
```
→ `201 Created` `{"agent_id":"hermes-spfx-builder","status":"active"}`

## Heartbeat
```bash
curl -X POST https://workswithagents.dev/v1/agents/hermes-spfx-builder/heartbeat -H "Content-Type: application/json" -d '{"load":0.67,"current_tasks":2,"state":"healthy","timestamp":"2026-06-20T12:00:00Z"}'
```
→ `200 OK`

## Query by Capability
```bash
curl "https://workswithagents.dev/v1/agents?action=build&target=spfx"
```
→ `{"agents":[...], "count":2, "recommended":"hermes-spfx-builder"}`

## Deregister
```bash
curl -X DELETE https://workswithagents.dev/v1/agents/hermes-spfx-builder
```
→ `204 No Content`
