"""
Portfolio version of secure messaging helpers adapted from a chat feature.

In the original project, message content was encrypted before being stored in
the database and decrypted when displayed back to authenticated users. The app
accepted an environment-provided key and needed safe fallback behavior when the
key was missing or invalid.

This public demo keeps the same Fernet-based approach in a smaller utility
module so the security-minded Python logic can be reviewed independently.
"""

from __future__ import annotations

import base64
import os

from cryptography.fernet import Fernet


ENC_PREFIX = "enc:v1:"


def generate_demo_key() -> str:
    return Fernet.generate_key().decode("utf-8")


def _build_fernet(key: str | None = None) -> Fernet | None:
    raw_key = key or os.getenv("SHOWCASE_MESSAGE_KEY", "")
    if not raw_key:
        return None

    key_bytes = raw_key.encode("utf-8")
    try:
        return Fernet(key_bytes)
    except Exception:
        # Accept passphrase-like input for demo convenience by reshaping it
        # into a valid Fernet key instead of failing hard.
        derived = base64.urlsafe_b64encode(key_bytes.ljust(32, b"0")[:32])
        return Fernet(derived)


def encrypt_message(plaintext: str, *, key: str | None = None) -> str:
    if not plaintext:
        return plaintext
    if plaintext.startswith(ENC_PREFIX):
        return plaintext

    fernet = _build_fernet(key)
    if not fernet:
        # Falling back to plaintext keeps the demo usable even when a reviewer
        # has not configured an environment key yet.
        return plaintext

    token = fernet.encrypt(plaintext.encode("utf-8")).decode("utf-8")
    return f"{ENC_PREFIX}{token}"


def decrypt_message(ciphertext: str | None, *, key: str | None = None) -> str:
    if not ciphertext:
        return ""
    if not ciphertext.startswith(ENC_PREFIX):
        return ciphertext

    fernet = _build_fernet(key)
    if not fernet:
        return "[Encrypted message unavailable]"

    token = ciphertext[len(ENC_PREFIX):]
    try:
        return fernet.decrypt(token.encode("utf-8")).decode("utf-8")
    except Exception:
        return "[Encrypted message unavailable]"
