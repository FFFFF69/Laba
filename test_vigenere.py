from vigenere import vigenere_encrypt, vigenere_decrypt


def test_encrypt_decrypt_ru():
    text = "Привет, мир!"
    key = "ключ"
    assert vigenere_decrypt(vigenere_encrypt(text, key), key) == text


def test_encrypt_decrypt_en():
    text = "Hello, world!"
    key = "key"
    assert vigenere_decrypt(vigenere_encrypt(text, key), key) == text


def test_non_letters_unchanged():
    assert vigenere_encrypt("123 !?", "ключ") == "123 !?"


def test_empty_key():
    try:
        vigenere_encrypt("abc", "")
        assert False, "Должно было возникнуть исключение"
    except ValueError:
        pass


if __name__ == "__main__":
    test_encrypt_decrypt_ru()
    test_encrypt_decrypt_en()
    test_non_letters_unchanged()
    test_empty_key()
    print("Все тесты пройдены")
