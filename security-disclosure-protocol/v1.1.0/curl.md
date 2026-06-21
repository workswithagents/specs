# Security Disclosure Protocol — cURL Examples

## Submit Finding
```bash
curl -X POST https://workswithagents.dev/v1/security-disclosure/submit-finding \
  -H "Content-Type: application/json" \
  -d '{}'
```

## Embargo Finding
```bash
curl -X POST https://workswithagents.dev/v1/security-disclosure/embargo-finding \
  -H "Content-Type: application/json" \
  -d '{}'
```

## Notify Vendor
```bash
curl -X POST https://workswithagents.dev/v1/security-disclosure/notify-vendor \
  -H "Content-Type: application/json" \
  -d '{}'
```

## Publish Disclosure
```bash
curl -X POST https://workswithagents.dev/v1/security-disclosure/publish-disclosure \
  -H "Content-Type: application/json" \
  -d '{}'
```
