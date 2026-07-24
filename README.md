# Infra Workspace — Presales Infrastructure Toolkit

**Febriyansyah** — Presales Specialist, PT. Citra Sentosa Solusindo

Infrastructure toolkit for presales demos, POCs, and client deployments.

## Projects

| Project | Description | Tests |
|---|---|---|
| `projects/net_discovery/` | Network discovery & inventory (ping, SNMP, port scan) | 6 ✅ |
| `projects/docker_stacks/` | Docker Compose templates (nginx, app, db, monitoring) | 4 ✅ |
| `projects/monitor_agent/` | System health checker (CPU, memory, disk, alert) | 6 ✅ |
| `projects/storage_health/` | Storage monitoring (disk usage, SMART, IOPS) | 6 ✅ |
| `projects/iac_scripts/` | IaC templates (cloud-init, setup automation) | 4 ✅ |
| `projects/vault_secrets/` | Encrypted secrets manager | 4 ✅ |

## Setup

```bash
pip install -r requirements.txt
```

## Test

```bash
python -m pytest projects/ -v
```
