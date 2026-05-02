"""
These tests explain the original context for the encryption helper.

In the private project, chat messages were encrypted before being saved so the
database did not store readable message bodies by default. When the correct key
was available, the application could decrypt content for authorized readers.

This test demonstrates that same round-trip behavior in a small public module.
"""

from showcase.message_crypto import decrypt_message, encrypt_message, generate_demo_key


def test_encrypt_and_decrypt_round_trip():
    # The public demo keeps the same core promise as the original feature:
    # plaintext goes in, encrypted storage comes out, and the message is
    # recoverable only with the correct key material.
    key = generate_demo_key()

    encrypted = encrypt_message("Hello portfolio", key=key)
    decrypted = decrypt_message(encrypted, key=key)

    assert encrypted.startswith("enc:v1:")
    assert decrypted == "Hello portfolio"
