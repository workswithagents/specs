# Coordination Protocol (ACP) — cURL Examples

## Elect Leader
```bash
curl -X POST https://workswithagents.dev/v1/coordination/elect-leader \
  -H "Content-Type: application/json" \
  -d '{}'
```

## Distribute Work
```bash
curl -X POST https://workswithagents.dev/v1/coordination/distribute-work \
  -H "Content-Type: application/json" \
  -d '{}'
```

## Steal Work
```bash
curl -X POST https://workswithagents.dev/v1/coordination/steal-work \
  -H "Content-Type: application/json" \
  -d '{}'
```

## Heartbeat
```bash
curl -X POST https://workswithagents.dev/v1/coordination/heartbeat \
  -H "Content-Type: application/json" \
  -d '{}'
```
