"""
ZeroTrace Merkle Tree & Salted State Manifest Verification Engine.
Implements domain-separated Merkle trees with odd-node duplication (RFC 6962 / Bitcoin pattern).
"""

from __future__ import annotations
import hashlib
import hmac
from typing import Any, Dict, List, Optional, Tuple


LEAF_DOMAIN_SEPARATOR = b"\x00"
NODE_DOMAIN_SEPARATOR = b"\x01"


def compute_leaf_hash(
    job_salt_hex: str,
    layer: str,
    object_id: str,
    content_hash: str,
    prefix_action: Optional[str] = None,
) -> str:
    """
    Computes domain-separated HMAC-SHA256 leaf hash for a state manifest item.
    """
    job_salt_bytes = bytes.fromhex(job_salt_hex)
    if prefix_action:
        raw_str = f"{prefix_action}:{layer}:{object_id}:{content_hash}"
    else:
        raw_str = f"{layer}:{object_id}:{content_hash}"
    payload = LEAF_DOMAIN_SEPARATOR + raw_str.encode("utf-8")
    return hmac.new(job_salt_bytes, payload, hashlib.sha256).hexdigest()


def build_merkle_root(leaf_hashes: List[str]) -> str:
    """
    Builds a deterministic Merkle root from a list of leaf hex hashes.
    1. Sorts leaves canonically (lexicographically).
    2. Duplicates the last node if a level has an odd number of nodes.
    3. Hashes pairs using domain separator 0x01.
    """
    if not leaf_hashes:
        return "0" * 64

    # Canonical sorting
    current_level = sorted(leaf_hashes)

    if len(current_level) == 1:
        return current_level[0]

    while len(current_level) > 1:
        next_level: List[str] = []
        # If odd, duplicate the last element
        if len(current_level) % 2 != 0:
            current_level.append(current_level[-1])

        for i in range(0, len(current_level), 2):
            left_bytes = bytes.fromhex(current_level[i])
            right_bytes = bytes.fromhex(current_level[i + 1])
            parent = hashlib.sha256(
                NODE_DOMAIN_SEPARATOR + left_bytes + right_bytes
            ).hexdigest()
            next_level.append(parent)

        current_level = next_level

    return current_level[0]


def compute_manifest_root(items: List[Dict[str, Any]], job_salt_hex: str) -> Tuple[str, List[str]]:
    """
    Computes the salted Merkle root for a full manifest of items.
    Returns (root_hex, list_of_leaf_hashes).
    """
    leaves: List[str] = []
    for item in items:
        leaf = compute_leaf_hash(
            job_salt_hex=job_salt_hex,
            layer=item["layer"],
            object_id=item["object_id"],
            content_hash=item["content_hash"],
        )
        leaves.append(leaf)
    root = build_merkle_root(leaves)
    return root, leaves


def compute_diff_root(
    pre_items: List[Dict[str, Any]],
    post_items: List[Dict[str, Any]],
    job_salt_hex: str,
) -> Tuple[str, List[str]]:
    """
    Computes diff root over:
    - Items destroyed (present in pre, absent in post) -> action ERASED
    - Items placed in retention vault -> action HELD
    """
    post_keys = {
        (item["layer"], item["object_id"]): item["content_hash"]
        for item in post_items
    }

    diff_leaves: List[str] = []

    # 1. Erased items
    for item in pre_items:
        key = (item["layer"], item["object_id"])
        if key not in post_keys:
            leaf = compute_leaf_hash(
                job_salt_hex=job_salt_hex,
                layer=item["layer"],
                object_id=item["object_id"],
                content_hash=item["content_hash"],
                prefix_action="ERASED",
            )
            diff_leaves.append(leaf)

    # 2. Held items
    for item in post_items:
        if item.get("held", False):
            leaf = compute_leaf_hash(
                job_salt_hex=job_salt_hex,
                layer=item["layer"],
                object_id=item["object_id"],
                content_hash=item["content_hash"],
                prefix_action="HELD",
            )
            diff_leaves.append(leaf)

    root = build_merkle_root(diff_leaves)
    return root, diff_leaves


def compute_subject_commitment(subject_salt_hex: str, canonical_subject: str) -> str:
    """
    Computes SHA-256(subject_salt || canonical_subject).
    """
    salt_bytes = bytes.fromhex(subject_salt_hex)
    payload = salt_bytes + canonical_subject.encode("utf-8")
    return hashlib.sha256(payload).hexdigest()
