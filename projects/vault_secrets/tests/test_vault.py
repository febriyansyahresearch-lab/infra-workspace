import pytest
import os
import tempfile
from projects.vault_secrets.src.vault import Vault, derive_key, encrypt_secret, decrypt_secret


def test_encrypt_decrypt():
    password = "testpass"
    salt = os.urandom(16)
    key = derive_key(password, salt)
    original = "my_secret_value"
    encrypted = encrypt_secret(original, key)
    decrypted = decrypt_secret(encrypted, key)
    assert decrypted == original


def test_vault_set_get():
    v = Vault("master123")
    v.set("db_password", "supersecret")
    assert v.get("db_password") == "supersecret"


def test_vault_get_nonexistent():
    v = Vault("master123")
    assert v.get("nonexistent") is None


def test_vault_list_keys():
    v = Vault("master123")
    v.set("key1", "val1")
    v.set("key2", "val2")
    assert set(v.list_keys()) == {"key1", "key2"}
