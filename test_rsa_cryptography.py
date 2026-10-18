from rsa_cryptography import (
    generate_keys,
    save_keys,
    encrypt_message,
    decrypt_message,
)

import os


def test_generate_keys():
    private_key, public_key = generate_keys()
    assert private_key is not None
    assert public_key is not None


def test_encrypt_decrypt_ru():
    private_key, public_key = generate_keys()
    message = "Это секретное сообщение"
    encrypted = encrypt_message(public_key, message)
    assert decrypt_message(private_key, encrypted) == message


def test_encrypt_decrypt_en():
    private_key, public_key = generate_keys()
    message = "Hello, world!"
    encrypted = encrypt_message(public_key, message)
    assert decrypt_message(private_key, encrypted) == message


def test_encrypted_differs_from_plaintext():
    private_key, public_key = generate_keys()
    message = "секрет"
    encrypted = encrypt_message(public_key, message)
    assert encrypted != message.encode("utf-8")


def test_save_keys_creates_files():
    private_key, public_key = generate_keys()
    save_keys(private_key, public_key,
              private_path="test_private.pem",
              public_path="test_public.pem")
    assert os.path.exists("test_private.pem")
    assert os.path.exists("test_public.pem")

    # уборка
    os.remove("test_private.pem")
    os.remove("test_public.pem")


if __name__ == "__main__":
    test_generate_keys()
    test_encrypt_decrypt_ru()
    test_encrypt_decrypt_en()
    test_encrypted_differs_from_plaintext()
    test_save_keys_creates_files()
    print("Все тесты пройдены")