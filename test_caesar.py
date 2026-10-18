from caesar import caesar_encrypt, caesar_decrypt


def test_encrypt_decrypt_ru():
    text = "Привет, мир!"
    shift = 3
    assert caesar_decrypt(caesar_encrypt(text, shift), shift) == text


def test_encrypt_decrypt_en():
    text = "Hello, world!"
    shift = 3
    assert caesar_decrypt(caesar_encrypt(text, shift), shift) == text


def test_non_letters_unchanged():
    assert caesar_encrypt("123 !?", 3) == "123 !?"


def test_shift_zero():
    text = "Привет, мир!"
    assert caesar_encrypt(text, 0) == text


def test_shift_full_alphabet():
    # Сдвиг на длину алфавита возвращает исходные символы
    assert caesar_encrypt("abc", 26) == "abc"
    assert caesar_encrypt("абв", 33) == "абв"


def test_yo_letter():
    # Проверка, что буква ё обрабатывается
    assert caesar_decrypt(caesar_encrypt("ёжик", 3), 3) == "ёжик"


if __name__ == "__main__":
    test_encrypt_decrypt_ru()
    test_encrypt_decrypt_en()
    test_non_letters_unchanged()
    test_shift_zero()
    test_shift_full_alphabet()#добавил
    test_yo_letter()#добавил
    print("Все тесты пройдены")