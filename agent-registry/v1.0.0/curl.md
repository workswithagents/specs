# Agent Registry — cURL Examples

## Register
```bash
curl -X POST https://workswithagents.dev/v1/registry/register -H "Content-Type: application/json" -d '{"agent_id":"deploy-bot-v2","public_key":"ed25519:abc123...","capabilities":["deploy:staging","deploy:production"],"owner":"admin@example.com","signature":"ed25519:base64sig..."}'
```
→ `201 Created` `{"agent_id":"deploy-bot-v2","status":"active","registered_at":"..."}`

## Get Agent
```bash
curl https://workswithagents.dev/v1/registry/deploy-bot-v2
```
→ `{"agent_id":"deploy-bot-v2","public_key":"ed25519:abc123...","capabilities":["deploy:staging"],"status":"active"}`

## Query
```bash
curl "https://workswithagents.dev/v1/registry?capability=deploy:staging&status=active"
```
→ `{"agents":[...]}`

## Update Capabilities
```bash
curl -X PATCH https://workswithagents.dev/v1/registry/deploy-bot-v2/capabilities -H "Content-Type: application/json" -d '{"capabilities":["deploy:staging","deploy:production","monitor:health"],"signature":"ed25519:..."}'
```
→ `200 OK`

## Suspend
```bash
curl -X POST https://workswithagents.dev/v1/registry/deploy-bot-v2/suspend -H "Content-Type: application/json" -d '{"reason":"security review","initiated_by":"admin@example.com"}'
```

## Revoke
```bash
curl -X POST https://workswithagents.dev/v1/registry/deploy-bot-v2/revoke -H "Content-Type: application/json" -d '{"reason":"compromised","initiated_by":"admin@example.com","reassign_pending":true}'
```

## Audit Log
```bash
curl https://workswithagents.dev/v1/registry/deploy-bot-v2/audit
```
