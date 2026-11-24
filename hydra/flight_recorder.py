"""
HYDRA Merkle Flight Recorder & Cryptographic Proof Engine
Maintains an append-only cryptographic Merkle Tree over all swarm events,
IPC frames, auction bids, and consensus blocks.
Provides O(log N) inclusion proofs for non-repudiable audit trails.
"""

import os
import json
import time
import hashlib
from typing import Dict, Any, List, Optional

FLIGHT_LOG_PATH = "/Users/lovelogic/OpenBot/Shared/hydra_merkle_flight_log.jsonl"

def sha256_hex(data: str) -> str:
    return hashlib.sha256(data.encode("utf-8")).hexdigest()

class MerkleTree:
    """Cryptographic binary Merkle Tree implementation."""

    def __init__(self, leaves: List[str]):
        self.leaves = leaves or [sha256_hex("EMPTY_ROOT")]
        self.layers = self._build_tree(self.leaves)

    def _build_tree(self, current_layer: List[str]) -> List[List[str]]:
        layers = [current_layer]
        while len(current_layer) > 1:
            next_layer = []
            for i in range(0, len(current_layer), 2):
                left = current_layer[i]
                right = current_layer[i + 1] if i + 1 < len(current_layer) else left
                combined = sha256_hex(left + right)
                next_layer.append(combined)
            layers.append(next_layer)
            current_layer = next_layer
        return layers

    @property
    def root(self) -> str:
        return self.layers[-1][0] if self.layers and self.layers[-1] else sha256_hex("EMPTY")

    def get_inclusion_proof(self, leaf_index: int) -> List[Dict[str, Any]]:
        """Generates an O(log N) inclusion audit path for a given leaf index."""
        if not (0 <= leaf_index < len(self.leaves)):
            raise IndexError("Leaf index out of range")
        proof = []
        idx = leaf_index
        for layer in self.layers[:-1]:
            is_right = (idx % 2 == 1)
            sibling_idx = idx - 1 if is_right else idx + 1
            if sibling_idx < len(layer):
                sibling = layer[sibling_idx]
            else:
                sibling = layer[idx]
            proof.append({
                "sibling": sibling,
                "position": "left" if is_right else "right"
            })
            idx = idx // 2
        return proof

    @staticmethod
    def verify_inclusion_proof(leaf_hash: str, proof: List[Dict[str, Any]], expected_root: str) -> bool:
        """Verifies an inclusion proof against an expected Merkle root."""
        current = leaf_hash
        for step in proof:
            sibling = step["sibling"]
            if step["position"] == "left":
                current = sha256_hex(sibling + current)
            else:
                current = sha256_hex(current + sibling)
        return current == expected_root


class SwarmFlightRecorder:
    def __init__(self, log_path: str = FLIGHT_LOG_PATH):
        self.log_path = log_path

    def record_event(self, event_type: str, actor: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Appends a cryptographically sealed event to the flight recorder log."""
        ts = time.time()
        raw_string = f"{ts}:{event_type}:{actor}:{json.dumps(payload, sort_keys=True)}"
        leaf_hash = sha256_hex(raw_string)

        entry = {
            "index": int(ts * 1000),
            "timestamp": ts,
            "event_type": event_type,
            "actor": actor,
            "payload": payload,
            "leaf_hash": leaf_hash
        }

        try:
            os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
            with open(self.log_path, "a") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception:
            pass

        return entry

    def compute_merkle_root(self) -> str:
        """Reads all recorded leaf hashes and computes the live Merkle root."""
        leaf_hashes = []
        if os.path.exists(self.log_path):
            try:
                with open(self.log_path, "r") as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            obj = json.loads(line)
                            leaf_hashes.append(obj.get("leaf_hash", sha256_hex(line)))
            except Exception:
                pass

        tree = MerkleTree(leaf_hashes)
        return tree.root

    def verify_event_integrity(self) -> Dict[str, Any]:
        """Audits the flight log for tampering or corrupted entries."""
        total = 0
        valid = 0
        if os.path.exists(self.log_path):
            with open(self.log_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    total += 1
                    try:
                        entry = json.loads(line)
                        ts = entry["timestamp"]
                        etype = entry["event_type"]
                        actor = entry["actor"]
                        raw_str = f"{ts}:{etype}:{actor}:{json.dumps(entry['payload'], sort_keys=True)}"
                        expected = sha256_hex(raw_str)
                        if expected == entry.get("leaf_hash"):
                            valid += 1
                    except Exception:
                        pass

        root = self.compute_merkle_root()
        return {
            "total_events": total,
            "valid_events": valid,
            "integrity_percent": 100.0 if total == 0 else round((valid / total) * 100.0, 2),
            "merkle_root": root,
            "status": "VERIFIED_SECURE" if (total == valid) else "CORRUPTION_DETECTED"
        }
