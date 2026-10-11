def caesar_encrypt(text, shift):
    encrypted_text = ""
    for char in text:
        if char.isalpha():
            if 'а' <= char.lower() <= 'я' or char.lower() == 'ё':
                alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
            else:
                alphabet = 'abcdefghijklmnopqrstuvwxyz'

            lower_char = char.lower()
            idx = alphabet.index(lower_char)
            new_idx = (idx + shift) % len(alphabet)
            new_char = alphabet[new_idx]

            if char.isupper():
                new_char = new_char.upper()
            encrypted_text += new_char
        else:
            encrypted_text += char
    return encrypted_text


def caesar_decrypt(encrypted_text, shift):
    return caesar_encrypt(encrypted_text, -shift)


# Пример использования
text = "Привет, мир!"
shift = 3
encrypted = caesar_encrypt(text, shift)
decrypted = caesar_decrypt(encrypted, shift)
print(f"Зашифровано: {encrypted}")
print(f"Расшифровано: {decrypted}")