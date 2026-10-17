"""
ZeroTrace Ed25519 Digital Signing and Verification Engine.
Handles deterministic receipt canonicalization, hashing, signing, and verification.
"""

from __future__ import annotations
import hashlib
import json
from typing import Any, Dict, Tuple
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.exceptions import InvalidSignature


def generate_ed25519_keypair() -> Tuple[str, str]:
    """
    Generates a new Ed25519 keypair.
    Returns (private_key_hex, public_key_hex).
    Private key is 32 raw bytes (64 hex characters).
    Public key is 32 raw bytes (64 hex characters).
    """
    private_key = ed25519.Ed25519PrivateKey.generate()
    private_bytes = private_key.private_bytes_raw()
    public_bytes = private_key.public_key().public_bytes_raw()
    return private_bytes.hex(), public_bytes.hex()


def canonicalize_receipt(receipt_data: Dict[str, Any]) -> bytes:
    """
    Produces canonical UTF-8 JSON representation with sorted keys and no whitespace.
    Excludes the 'signature' field if present.
    """
    payload = {k: v for k, v in receipt_data.items() if k != "signature"}
    canonical_str = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return canonical_str.encode("utf-8")


def compute_receipt_digest(receipt_data: Dict[str, Any]) -> bytes:
    """
    Computes SHA-256 digest of canonical receipt JSON.
    """
    canonical_bytes = canonicalize_receipt(receipt_data)
    return hashlib.sha256(canonical_bytes).digest()


def sign_receipt(receipt_data: Dict[str, Any], private_key_hex: str) -> str:
    """
    Signs the SHA-256 digest of the canonical receipt with Ed25519 private key.
    Returns 64-byte signature encoded as 128 hex characters.
    """
    private_bytes = bytes.fromhex(private_key_hex)
    private_key = ed25519.Ed25519PrivateKey.from_private_bytes(private_bytes)
    digest = compute_receipt_digest(receipt_data)
    signature_bytes = private_key.sign(digest)
    return signature_bytes.hex()


def verify_receipt_signature(receipt_data: Dict[str, Any]) -> bool:
    """
    Verifies Ed25519 digital signature of receipt using receipt_data['signer_public_key']
    and receipt_data['signature'].
    """
    try:
        pub_key_hex = receipt_data["signer_public_key"]
        sig_hex = receipt_data["signature"]
        pub_bytes = bytes.fromhex(pub_key_hex)
        sig_bytes = bytes.fromhex(sig_hex)

        public_key = ed25519.Ed25519PublicKey.from_public_bytes(pub_bytes)
        digest = compute_receipt_digest(receipt_data)
        public_key.verify(sig_bytes, digest)
        return True
    except (InvalidSignature, KeyError, ValueError):
        return False
