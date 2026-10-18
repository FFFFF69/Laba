import os
import tempfile
import pytest
from cryptography.fernet import Fernet

from file_crypto import (
    generate_key,
    load_key,
    encrypt_file,
    decrypt_file,
)


@pytest.fixture
def tmp_file():
    fd, path = tempfile.mkstemp()
    with os.fdopen(fd, "wb") as f:
        f.write(b"test data 123")
    yield path
    if os.path.exists(path):
        os.remove(path)
    if os.path.exists(path + ".bak"):
        os.remove(path + ".bak")


def test_generate_and_load_key(tmp_path):
    key_path = str(tmp_path / "test.key")
    key = generate_key(key_path)
    assert os.path.exists(key_path)
    loaded = load_key(key_path)
    assert loaded == key


def test_encrypt_decrypt_roundtrip(tmp_file):
    key = Fernet.generate_key()

    with open(tmp_file, "rb") as f:
        original = f.read()

    encrypt_file(tmp_file, key)

    with open(tmp_file, "rb") as f:
        encrypted = f.read()
    assert encrypted != original

    decrypt_file(tmp_file, key)

    with open(tmp_file, "rb") as f:
        restored = f.read()
    assert restored == original


def test_encrypt_nonexistent_file():
    key = Fernet.generate_key()
    with pytest.raises(FileNotFoundError):
        encrypt_file("no_such_file_12345.txt", key)


def test_decrypt_wrong_key(tmp_file):
    key1 = Fernet.generate_key()
    key2 = Fernet.generate_key()

    encrypt_file(tmp_file, key1)

    with pytest.raises(ValueError):
        decrypt_file(tmp_file, key2)


def test_load_missing_key():
    with pytest.raises(FileNotFoundError):
        load_key("no_such_key_12345.key")
