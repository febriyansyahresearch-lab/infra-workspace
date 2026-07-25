# Vault Secrets — Encrypted Secrets Manager

**Use Case:** Secure credential management for client demos  
**Algorithm:** AES-256 via Fernet (PBKDF2 key derivation)

## Usage
```bash
export VAULT_PASSWORD=mypass
python -m projects.vault_secrets.src.vault init
python -m projects.vault_secrets.src.vault set --key db_pass --value secret123
python -m projects.vault_secrets.src.vault get --key db_pass
python -m projects.vault_secrets.src.vault list
```
