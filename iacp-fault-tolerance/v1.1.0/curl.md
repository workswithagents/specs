# IACP Fault Tolerance — cURL Examples

## Detect Timeout
```bash
curl -X POST https://workswithagents.dev/v1/iacp/fault-tolerance/detect-timeout \
  -H "Content-Type: application/json" \
  -d '{}'
```

## Handle Dead Letter
```bash
curl -X POST https://workswithagents.dev/v1/iacp/fault-tolerance/handle-dead-letter \
  -H "Content-Type: application/json" \
  -d '{}'
```

## Rollback
```bash
curl -X POST https://workswithagents.dev/v1/iacp/fault-tolerance/rollback \
  -H "Content-Type: application/json" \
  -d '{}'
```

## Retry With Backoff
```bash
curl -X POST https://workswithagents.dev/v1/iacp/fault-tolerance/retry-with-backoff \
  -H "Content-Type: application/json" \
  -d '{}'
```
