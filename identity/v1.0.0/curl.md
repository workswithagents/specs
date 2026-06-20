# Identity Protocol — cURL Examples

cURL command examples for the Identity Protocol (v1.0.0).

## 1. Register Identity

```bash
curl -X POST https://workswithagents.dev/v1/identity/register \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "hermes-spfx-builder",
    "public_key": "abc123def4567890abcdef1234567890abcdef1234567890abcdef1234567890",
    "identity_version": "1.0.0",
    "owner": {
      "name": "Vilius Vystartas",
      "email": "agent@example.com"
    }
  }'
```

**Expected response (201 Created):**
```json
{
  "agent_id": "hermes-spfx-builder",
  "status": "active",
  "public_key": "abc123def4567890...",
  "registered_at": "2026-06-20T12:00:00Z"
}
```

## 2. Get Identity (Public Key + Status)

```bash
curl https://workswithagents.dev/v1/identity/hermes-spfx-builder \
  -H "Accept: application/json"
```

**Expected response (200 OK):**
```json
{
  "agent_id": "hermes-spfx-builder",
  "public_key": "abc123def4567890abcdef1234567890abcdef1234567890abcdef1234567890",
  "status": "active",
  "created_at": "2026-05-05T21:00:00Z",
  "expires_at": null
}
```

## 3. Verify a Signed Message

Submit a signed message for server-side verification.

```bash
curl -X POST https://workswithagents.dev/v1/identity/verify \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "hermes-spfx-builder",
    "message": {
      "agent_id": "hermes-spfx-builder",
      "timestamp": "2026-06-20T12:00:00Z",
      "payload": {
        "type": "heartbeat",
        "status": "healthy",
        "load": 0.3
      }
    },
    "signature": "ed25519:a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2..."
  }'
```

**Expected response (200 OK):**
```json
{
  "valid": true,
  "agent_id": "hermes-spfx-builder",
  "status": "active",
  "verified_at": "2026-06-20T12:00:05Z"
}
```

**Invalid signature response (200 OK):**
```json
{
  "valid": false,
  "agent_id": "hermes-spfx-builder",
  "reason": "signature_mismatch"
}
```

## 4. Rotate Keys

```bash
# First generate new keypair, then submit rotation signed with OLD key
curl -X POST https://workswithagents.dev/v1/identity/hermes-spfx-builder/rotate \
  -H "Content-Type: application/json" \
  -d '{
    "new_public_key": "fed9876543210fedcba9876543210fedcba9876543210fedcba9876543210fedc",
    "signed_by": "ed25519:signed_with_old_private_key...",
    "rotation_message": {
      "agent_id": "hermes-spfx-builder",
      "timestamp": 1750348800,
      "payload": {
        "type": "key_rotation",
        "new_public_key": "fed9876543210fedcba9876543210fedcba9876543210fedcba9876543210fedc"
      }
    }
  }'
```

**Expected response (200 OK):**
```json
{
  "status": "rotating",
  "old_key_expires": "2026-06-21T12:00:00Z"
}
```

## 5. Revoke Identity

```bash
curl -X POST https://workswithagents.dev/v1/identity/hermes-spfx-builder/revoke \
  -H "Content-Type: application/json" \
  -d '{
    "reason": "compromised",
    "signed_by": "ed25519:a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2..."
  }'
```

**Expected response (200 OK):**
```json
{
  "status": "revoked",
  "revoked_at": "2026-06-20T12:30:00Z",
  "reason": "compromised",
  "pending_tasks_reassigned": true
}
```

## API Summary

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| POST | `/v1/identity/register` | Register new agent identity | None |
| GET | `/v1/identity/{agent_id}` | Look up identity + status | None |
| POST | `/v1/identity/verify` | Verify a signed message | None |
| POST | `/v1/identity/{agent_id}/rotate` | Rotate keys (signed by old key) | Signature |
| POST | `/v1/identity/{agent_id}/revoke` | Revoke identity (signed by own key) | Signature |
