from showcase.message_crypto import decrypt_message, encrypt_message, generate_demo_key


def test_encrypt_and_decrypt_round_trip():
    key = generate_demo_key()

    encrypted = encrypt_message("Hello portfolio", key=key)
    decrypted = decrypt_message(encrypted, key=key)

    assert encrypted.startswith("enc:v1:")
    assert decrypted == "Hello portfolio"
