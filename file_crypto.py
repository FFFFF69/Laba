import os
from cryptography.fernet import Fernet, InvalidToken


def generate_key(path: str = "secret.key") -> bytes:
    key = Fernet.generate_key()
    with open(path, "wb") as f:
        f.write(key)
    return key


def load_key(path: str = "secret.key") -> bytes:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Файл ключа не найден: {path}")
    with open(path, "rb") as f:
        return f.read()


def encrypt_file(file_path: str, key: bytes) -> str:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл не найден: {file_path}")

    cipher = Fernet(key)

    with open(file_path, "rb") as f:
        data = f.read()

    encrypted = cipher.encrypt(data)

    backup_path = file_path + ".bak"
    with open(backup_path, "wb") as f:
        f.write(data)

    with open(file_path, "wb") as f:
        f.write(encrypted)

    return backup_path


def decrypt_file(file_path: str, key: bytes) -> None:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл не найден: {file_path}")

    cipher = Fernet(key)

    with open(file_path, "rb") as f:
        encrypted = f.read()

    try:
        decrypted = cipher.decrypt(encrypted)
    except InvalidToken:
        raise ValueError("Не удалось расшифровать: неверный ключ или файл повреждён")

    with open(file_path, "wb") as f:
        f.write(decrypted)


if __name__ == "__main__":
    test_file = "secret.txt"

    if not os.path.exists(test_file):
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("Это секретное сообщение.\n")

    with open(test_file, "rb") as f:
        original = f.read()

    key = generate_key("secret.key")
    print(f"Ключ сохранён в secret.key ({len(key)} байт)")

    encrypt_file(test_file, key)
    print(f"Файл {test_file} зашифрован")

    decrypt_file(test_file, key)
    print(f"Файл {test_file} расшифрован")

    with open(test_file, "rb") as f:
        restored = f.read()

    assert restored == original, "Ошибка: содержимое не совпадает!"
    print("Проверка пройдена: содержимое восстановлено корректно")
