# Identity Protocol — Python Example

Complete Python implementation of the Identity Protocol (v1.0.0). Uses stdlib only.

```python
"""
Identity Protocol v1.0.0 — Python Reference Implementation

Full lifecycle: CREATE → REGISTER → ATTEST → VERIFY → ROTATE → REVOKE
Stdlib only. Uses cryptography library for Ed25519 operations.
"""
import json
import time
import uuid
import urllib.request
import urllib.error
from typing import Optional

# Requires: pip install cryptography
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization


class IdentityClient:
    """Agent identity management: keys, registration, signing, verification."""

    def __init__(self, agent_id: str, api_base: str = "https://workswithagents.dev"):
        self.agent_id = agent_id
        self.api_base = api_base.rstrip("/")
        self._private_key: Optional[ed25519.Ed25519PrivateKey] = None
        self._public_key_bytes: Optional[bytes] = None

    def _post(self, path: str, body: dict) -> dict:
        url = f"{self.api_base}{path}"
        data = json.dumps(body).encode()
        req = urllib.request.Request(url, data=data, method="POST",
            headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            error = json.loads(e.read())
            raise RuntimeError(f"Identity error ({e.code}): {error.get('detail', 'unknown')}")

    def _get(self, path: str) -> dict:
        url = f"{self.api_base}{path}"
        with urllib.request.urlopen(url) as resp:
            return json.loads(resp.read())

    # ── CREATE: Generate keypair ─────────────────────────────

    def create_keypair(self) -> dict:
        """Generate an Ed25519 keypair. Returns public key hex string."""
        self._private_key = ed25519.Ed25519PrivateKey.generate()
        pub_key = self._private_key.public_key()
        self._public_key_bytes = pub_key.public_bytes(
            serialization.Encoding.Raw,
            serialization.PublicFormat.Raw
        )
        return {
            "agent_id": self.agent_id,
            "public_key": self._public_key_bytes.hex(),
            "algorithm": "ed25519"
        }

    @property
    def public_key_hex(self) -> str:
        if not self._public_key_bytes:
            raise RuntimeError("No keypair. Call create_keypair() first.")
        return self._public_key_bytes.hex()

    def export_private_key_hex(self) -> str:
        """Export private key as hex (for backup — keep secure!)."""
        if not self._private_key:
            raise RuntimeError("No keypair. Call create_keypair() first.")
        return self._private_key.private_bytes(
            serialization.Encoding.Raw,
            serialization.PrivateFormat.Raw,
            serialization.NoEncryption()
        ).hex()

    # ── REGISTER ────────────────────────────────────────────

    def register(self, owner_name: Optional[str] = None,
                 owner_email: Optional[str] = None) -> dict:
        """Register identity in the agent registry."""
        body = {
            "agent_id": self.agent_id,
            "public_key": self.public_key_hex,
            "identity_version": "1.0.0"
        }
        if owner_name:
            body["owner"] = {"name": owner_name, "email": owner_email or ""}
        return self._post("/v1/identity/register", body)

    # ── SIGN messages ───────────────────────────────────────

    def sign_message(self, payload: dict) -> dict:
        """Sign a message with the agent's private key."""
        if not self._private_key:
            raise RuntimeError("No keypair. Call create_keypair() first.")

        message = {
            "agent_id": self.agent_id,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "payload": payload
        }
        message_bytes = json.dumps(message, sort_keys=True).encode()
        signature = self._private_key.sign(message_bytes).hex()

        return {
            "message": message,
            "signature": f"ed25519:{signature}"
        }

    # ── VERIFY another agent ─────────────────────────────────

    def verify_identity(self, signed_message: dict, other_agent_id: str) -> dict:
        """Verify a signed message from another agent."""
        # Fetch their public key from registry
        identity = self._get(f"/v1/identity/{other_agent_id}")
        pub_key_bytes = bytes.fromhex(identity["public_key"])
        public_key = ed25519.Ed25519PublicKey.from_public_bytes(pub_key_bytes)

        # Verify the signature
        message = signed_message["message"]
        message_bytes = json.dumps(message, sort_keys=True).encode()

        sig_hex = signed_message["signature"]
        if sig_hex.startswith("ed25519:"):
            sig_hex = sig_hex.split(":", 1)[1]
        signature_bytes = bytes.fromhex(sig_hex)

        try:
            public_key.verify(signature_bytes, message_bytes)
            return {
                "valid": True,
                "agent_id": other_agent_id,
                "status": identity.get("status", "active"),
                "verified_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            }
        except Exception:
            return {
                "valid": False,
                "agent_id": other_agent_id,
                "reason": "signature_mismatch"
            }

    # ── ROTATE keys ─────────────────────────────────────────

    def rotate_keypair(self) -> dict:
        """Generate new keypair and register rotation."""
        old_key = self._private_key
        new_pair = self.create_keypair()

        # Rotation is a signed operation using the old key
        rotation_msg = {
            "agent_id": self.agent_id,
            "timestamp": int(time.time()),
            "payload": {
                "type": "key_rotation",
                "new_public_key": self.public_key_hex
            }
        }
        msg_bytes = json.dumps(rotation_msg, sort_keys=True).encode()
        signature = old_key.sign(msg_bytes).hex()

        return self._post(f"/v1/identity/{self.agent_id}/rotate", {
            "new_public_key": new_pair["public_key"],
            "signed_by": f"ed25519:{signature}",
            "rotation_message": rotation_msg
        })

    # ── REVOKE ──────────────────────────────────────────────

    def revoke(self, reason: str = "compromised") -> dict:
        """Revoke this agent's identity."""
        if not self._private_key:
            raise RuntimeError("No keypair.")

        revoke_msg = {
            "agent_id": self.agent_id,
            "timestamp": int(time.time()),
            "payload": {
                "type": "revocation",
                "reason": reason
            }
        }
        msg_bytes = json.dumps(revoke_msg, sort_keys=True).encode()
        signature = self._private_key.sign(msg_bytes).hex()

        return self._post(f"/v1/identity/{self.agent_id}/revoke", {
            "reason": reason,
            "signed_by": f"ed25519:{signature}"
        })

    # ── LOOKUP ──────────────────────────────────────────────

    def lookup(self, target_agent_id: str) -> dict:
        """Look up another agent's identity and status."""
        return self._get(f"/v1/identity/{target_agent_id}")


# ── Demo ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Identity Protocol v1.0.0 Demo ===\n")

    # Step 1: CREATE — Generate keypair
    alice = IdentityClient("alice-builder-01")
    keypair = alice.create_keypair()
    print(f"1. Keypair generated:")
    print(f"   Agent:    {keypair['agent_id']}")
    print(f"   Pub key:  {keypair['public_key'][:40]}...")
    print(f"   Algo:     {keypair['algorithm']}")

    # Step 2: REGISTER — Register identity
    print(f"\n2. Registering identity...")
    try:
        result = alice.register(
            owner_name="Alice Engineer",
            owner_email="alice@workswithagents.dev"
        )
        print(f"   Status:  {result.get('status', 'registered')}")
    except RuntimeError as e:
        print(f"   API call (offline mode): {e}")

    # Step 3: SIGN — Sign a message
    print(f"\n3. Signing a message...")
    signed = alice.sign_message({
        "type": "heartbeat",
        "status": "healthy",
        "load": 0.3
    })
    print(f"   Message:   {signed['message']['payload']['type']}")
    print(f"   Signature: {signed['signature'][:50]}...")

    # Step 4: VERIFY — Verify another agent
    print(f"\n4. Verifying another agent's signature...")
    bob = IdentityClient("bob-reviewer-02")
    bob.create_keypair()
    bob_signed = bob.sign_message({"type": "query", "question": "Review ready?"})

    try:
        verification = alice.verify_identity(bob_signed, "bob-reviewer-02")
        print(f"   Valid:  {verification['valid']}")
        print(f"   Agent:  {verification.get('agent_id', 'N/A')}")
    except RuntimeError as e:
        print(f"   API call (offline mode): {e}")

    # Step 5: LOOKUP
    print(f"\n5. Looking up an agent's identity...")
    try:
        identity = alice.lookup("bob-reviewer-02")
        print(f"   Status: {identity.get('status', 'active')}")
        print(f"   Key:    {identity.get('public_key', 'N/A')[:40]}...")
    except RuntimeError as e:
        print(f"   API call (offline mode): {e}")

    # Step 6: ROTATE
    print(f"\n6. Rotating keys...")
    old_key_hex = alice.public_key_hex[:20]
    try:
        rotation = alice.rotate_keypair()
        print(f"   Old key:  {old_key_hex}...")
        print(f"   New key:  {alice.public_key_hex[:20]}...")
        print(f"   Status:   {rotation.get('status', 'rotating')}")
    except RuntimeError as e:
        print(f"   API call (offline mode): {e}")

    # Step 7: REVOKE
    print(f"\n7. Revoking (demo — not actually revoking)...")
    print(f"   POST /v1/identity/{alice.agent_id}/revoke")
    print(f"   Body: {{\"reason\": \"compromised\", ...}}")

    print("\n=== Lifecycle Complete ===")
    print("CREATE → REGISTER → SIGN → VERIFY → ROTATE → REVOKE")
```

## Security Notes

- Private keys are generated via `cryptography.hazmat.primitives.asymmetric.ed25519`
- Signatures use Ed25519 (RFC 8032)
- Replay protection: timestamps in messages, 60s tolerance
- Key rotation has a 24h grace period
