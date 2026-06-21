# AI Gateway / Policy Enforcement Point — cURL Examples

## Enforce Policy
```bash
curl -X POST https://workswithagents.dev/v1/gateway/enforce-policy \
  -H "Content-Type: application/json" \
  -d '{}'
```

## Check Rate Limit
```bash
curl -X POST https://workswithagents.dev/v1/gateway/check-rate-limit \
  -H "Content-Type: application/json" \
  -d '{}'
```

## Audit Request
```bash
curl -X POST https://workswithagents.dev/v1/gateway/audit-request \
  -H "Content-Type: application/json" \
  -d '{}'
```

## Block Request
```bash
curl -X POST https://workswithagents.dev/v1/gateway/block-request \
  -H "Content-Type: application/json" \
  -d '{}'
```
