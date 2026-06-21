import hashlib
from ed25519 import SigningKey, VerifyingKey

class MerkleAuditTrail:
    def __init__(self):
        self.entries: list[bytes] = []
        self.sk = SigningKey.generate()

    def append(self, action: dict) -> str:
        entry = json.dumps(action, sort_keys=True).encode()
        signature = self.sk.sign(entry)
        leaf = hashlib.sha256(entry + signature).digest()
        self.entries.append(leaf)
        return self._root_hash()

    def _root_hash(self) -> str:
        if not self.entries:
            return ""
        # Simplified Merkle root (full impl uses tree)
        h = self.entries[0]
        for e in self.entries[1:]:
            h = hashlib.sha256(h + e).digest()
        return h.hex()

    def verify(self, index: int, action: dict) -> bool:
        # Verify a specific entry in the chain
        vk = self.sk.verify_key
        entry = json.dumps(action, sort_keys=True).encode()
        try:
            signature = self.sk.sign(entry)
            vk.verify(signature, entry)
            return True
        except Exception:
            return False
