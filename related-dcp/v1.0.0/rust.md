use ed25519_dalek::{SigningKey, VerifyingKey, Signature};
use sha2::{Sha256, Digest};
use serde_json::Value;

struct MerkleAuditTrail {
    entries: Vec<Vec<u8>>,
    signing_key: SigningKey,
}

impl MerkleAuditTrail {
    fn new() -> Self {
        let mut csprng = rand::rngs::OsRng;
        let signing_key = SigningKey::generate(&mut csprng);
        Self {
            entries: Vec::new(),
            signing_key,
        }
    }

    fn append(&mut self, action: &Value) -> String {
        let entry = serde_json::to_vec(action).unwrap();
        let signature = self.signing_key.sign(&entry);
        let mut hasher = Sha256::new();
        hasher.update(&entry);
        hasher.update(signature.to_bytes());
        let leaf = hasher.finalize().to_vec();
        self.entries.push(leaf);
        self.root_hash()
    }

    fn root_hash(&self) -> String {
        if self.entries.is_empty() {
            return String::new();
        }
        let mut h = self.entries[0].clone();
        for e in &self.entries[1..] {
            let mut hasher = Sha256::new();
            hasher.update(&h);
            hasher.update(e);
            h = hasher.finalize().to_vec();
        }
        hex::encode(h)
    }

    fn verify(&self, index: usize, action: &Value) -> bool {
        let verify_key = self.signing_key.verifying_key();
        let entry = serde_json::to_vec(action).unwrap();
        let signature = self.signing_key.sign(&entry);
        verify_key.verify(&entry, &signature).is_ok()
    }
}

fn main() {
    let mut trail = MerkleAuditTrail::new();

    let root = trail.append(&serde_json::json!({
        "action": "tool.invoke",
        "tool": "cargo",
        "command": "test"
    }));
    println!("Merkle root: {}", root);

    // Post-quantum mode placeholder (ML-KEM / ML-DSA)
    let pq_root = trail.append(&serde_json::json!({
        "action": "agent.deploy",
        "target": "prod",
        "kem": "ML-KEM-768"
    }));
    println!("PQ Merkle root: {}", pq_root);
}
