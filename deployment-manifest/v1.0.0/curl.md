# Deployment Manifest — cURL Examples

## Deploy Fleet
```bash
curl -X POST https://workswithagents.dev/v1/deployment/deploy-fleet \
  -H "Content-Type: application/json" \
  -d '{}'
```

## Validate Manifest
```bash
curl -X POST https://workswithagents.dev/v1/deployment/validate-manifest \
  -H "Content-Type: application/json" \
  -d '{}'
```

## Scale Agents
```bash
curl -X POST https://workswithagents.dev/v1/deployment/scale-agents \
  -H "Content-Type: application/json" \
  -d '{}'
```

## Get Status
```bash
curl -X POST https://workswithagents.dev/v1/deployment/get-status \
  -H "Content-Type: application/json" \
  -d '{}'
```
