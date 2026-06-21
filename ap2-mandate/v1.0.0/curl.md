# AP2 Payment Mandate — cURL Examples

## Create Mandate
```bash
curl -X POST https://workswithagents.dev/v1/ap2/create-mandate \
  -H "Content-Type: application/json" \
  -d '{}'
```

## Verify Spend
```bash
curl -X POST https://workswithagents.dev/v1/ap2/verify-spend \
  -H "Content-Type: application/json" \
  -d '{}'
```

## Revoke Mandate
```bash
curl -X POST https://workswithagents.dev/v1/ap2/revoke-mandate \
  -H "Content-Type: application/json" \
  -d '{}'
```

## Get Spend History
```bash
curl -X POST https://workswithagents.dev/v1/ap2/get-spend-history \
  -H "Content-Type: application/json" \
  -d '{}'
```
