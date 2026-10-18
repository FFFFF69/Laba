from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend


def generate_keys(key_size: int = 2048):
    """Генерирует пару (private_key, public_key)."""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
        backend=default_backend(),
    )
    return private_key, private_key.public_key()


def save_keys(private_key, public_key,
              private_path: str = "private_key.pem",
              public_path: str = "public_key.pem"):
    """Сохраняет ключи в PEM-файлы."""
    with open(private_path, "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        ))

    with open(public_path, "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ))


def encrypt_message(public_key, message: str) -> bytes:
    """Шифрует строку открытым ключом."""
    return public_key.encrypt(
        message.encode("utf-8"),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )


def decrypt_message(private_key, encrypted_message: bytes) -> str:
    """Расшифровывает сообщение закрытым ключом."""
    decrypted = private_key.decrypt(
        encrypted_message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    return decrypted.decode("utf-8")


if __name__ == "__main__":
    private_key, public_key = generate_keys()
    save_keys(private_key, public_key)

    message = "Это секретное сообщение"
    encrypted = encrypt_message(public_key, message)
    print("Зашифрованное сообщение:", encrypted)

    decrypted = decrypt_message(private_key, encrypted)
    print("Расшифрованное сообщение:", decrypted)

    assert decrypted == message, "Ошибка: расшифровка не совпадает"