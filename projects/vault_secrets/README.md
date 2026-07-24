# Vault Secrets — Encrypted Secrets Manager

**Use Case:** Secure credential management for client demos  
**Algorithm:** AES-256 via Fernet (PBKDF2 key derivation)

## Usage
```bash
python -m projects.vault_secrets.src.vault init --password mypass
python -m projects.vault_secrets.src.vault set --password mypass --key db_pass --value secret123
python -m projects.vault_secrets.src.vault get --password mypass --key db_pass
python -m projects.vault_secrets.src.vault list --password mypass
```
