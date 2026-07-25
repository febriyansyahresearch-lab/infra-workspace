import os
import json
import base64
import getpass
from typing import Optional
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def derive_key(master_password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100_000)
    return base64.urlsafe_b64encode(kdf.derive(master_password.encode()))


def init_vault(password: str) -> dict:
    salt = os.urandom(16)
    key = derive_key(password, salt)
    store = {"salt": salt.hex(), "secrets": {}}
    return store


def encrypt_secret(plaintext: str, key: bytes) -> str:
    f = Fernet(key)
    return f.encrypt(plaintext.encode()).decode()


def decrypt_secret(ciphertext: str, key: bytes) -> str:
    f = Fernet(key)
    return f.decrypt(ciphertext.encode()).decode()


class Vault:
    def __init__(self, master_password: str):
        self.store = init_vault(master_password)
        self.key = derive_key(master_password, bytes.fromhex(self.store["salt"]))

    def set(self, key: str, value: str) -> None:
        self.store["secrets"][key] = encrypt_secret(value, self.key)

    def get(self, key: str) -> Optional[str]:
        if key not in self.store["secrets"]:
            return None
        return decrypt_secret(self.store["secrets"][key], self.key)

    def list_keys(self) -> list[str]:
        return list(self.store["secrets"].keys())

    def export(self, filepath: str) -> None:
        with open(filepath, "w") as f:
            json.dump(self.store, f)

    @classmethod
    def import_vault(cls, filepath: str, master_password: str) -> "Vault":
        with open(filepath) as f:
            store = json.load(f)
        v = cls.__new__(cls)
        v.store = store
        v.key = derive_key(master_password, bytes.fromhex(store["salt"]))
        return v


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Encrypted secrets vault")
    parser.add_argument("action", choices=["init", "set", "get", "list"])
    parser.add_argument("--password", help="Master password; prefer VAULT_PASSWORD or interactive prompt")
    parser.add_argument("--key", help="Secret key name")
    parser.add_argument("--value", help="Secret value")
    parser.add_argument("--file", default="vault.json", help="Vault file path")
    args = parser.parse_args()
    master_password = args.password or os.getenv("VAULT_PASSWORD") or getpass.getpass("Master password: ")

    if args.action == "init":
        v = Vault(master_password)
        v.export(args.file)
        print(f"Vault initialized: {args.file}")
    elif args.action in ("set", "get", "list"):
        v = Vault.import_vault(args.file, master_password)
        if args.action == "set":
            v.set(args.key, args.value)
            v.export(args.file)
            print(f"Secret set: {args.key}")
        elif args.action == "get":
            val = v.get(args.key)
            print(val if val else "Not found")
        else:
            for k in v.list_keys():
                print(k)
