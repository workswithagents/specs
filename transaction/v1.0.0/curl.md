# Transaction Protocol (ATP) — cURL Examples

## Create Transaction
```bash
curl -X POST https://workswithagents.dev/v1/transaction/create-transaction \
  -H "Content-Type: application/json" \
  -d '{}'
```

## Commit
```bash
curl -X POST https://workswithagents.dev/v1/transaction/commit \
  -H "Content-Type: application/json" \
  -d '{}'
```

## Rollback
```bash
curl -X POST https://workswithagents.dev/v1/transaction/rollback \
  -H "Content-Type: application/json" \
  -d '{}'
```

## Get Status
```bash
curl -X POST https://workswithagents.dev/v1/transaction/get-status \
  -H "Content-Type: application/json" \
  -d '{}'
```
