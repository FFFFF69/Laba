EN_LOWER = "abcdefghijklmnopqrstuvwxyz"
EN_UPPER = EN_LOWER.upper()
RU_LOWER = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
RU_UPPER = RU_LOWER.upper()


def _get_alphabets(char: str):
    """Возвращает (алфавит, размер) для символа."""
    if char in EN_LOWER or char in EN_UPPER:
        return (EN_LOWER, 26) if char.islower() else (EN_UPPER, 26)
    if char in RU_LOWER or char in RU_UPPER:
        return (RU_LOWER, 32) if char.islower() else (RU_UPPER, 32)
    return None, 0


def _shift_char(char: str, shift: int) -> str:
    """Сдвигает букву на shift позиций внутри её алфавита."""
    alphabet, size = _get_alphabets(char)
    if alphabet is None:
        return char  # не буква — возвращаем как есть
    idx = alphabet.index(char)
    return alphabet[(idx + shift) % size]


def vigenere_encrypt(text: str, key: str) -> str:
    """Шифрует текст шифром Виженера (латиница + кириллица)."""
    if not key or not key.isalpha():
        raise ValueError("Ключ должен состоять только из букв и быть непустым")

    result = ""
    key_index = 0

    for char in text:
        if char.isalpha():
            key_char = key[key_index % len(key)]
            alphabet, size = _get_alphabets(key_char)
            if alphabet is None:
                key_index += 1
                result += char
                continue
            shift = alphabet.index(key_char.lower() if key_char.isupper() else key_char)
            result += _shift_char(char, shift)
            key_index += 1
        else:
            result += char

    return result


def vigenere_decrypt(encrypted_text: str, key: str) -> str:
    """Расшифровывает текст, зашифрованный шифром Виженера."""
    if not key or not key.isalpha():
        raise ValueError("Ключ должен состоять только из букв и быть непустым")

    result = ""
    key_index = 0

    for char in encrypted_text:
        if char.isalpha():
            key_char = key[key_index % len(key)]
            alphabet, size = _get_alphabets(key_char)
            if alphabet is None:
                key_index += 1
                result += char
                continue
            shift = alphabet.index(key_char.lower() if key_char.isupper() else key_char)
            result += _shift_char(char, -shift)
            key_index += 1
        else:
            result += char

    return result


if __name__ == "__main__":
    text = "Привет, мир!"
    key = "ключ"

    encrypted = vigenere_encrypt(text, key)
    decrypted = vigenere_decrypt(encrypted, key)

    print(f"Исходный:     {text}")
    print(f"Зашифровано:  {encrypted}")
    print(f"Расшифровано: {decrypted}")

    assert decrypted == text, "Ошибка: расшифровка не совпадает"
