# Infra Workspace — Presales Infrastructure Toolkit

[![CI](https://github.com/febriyansyahresearch-lab/infra-workspace/actions/workflows/test.yml/badge.svg)](https://github.com/febriyansyahresearch-lab/infra-workspace/actions)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-20%20passed-brightgreen)](projects/)

**Febriyansyah** — Presales Specialist

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

## Usage

```bash
# Network discovery — ping sweep, port scan, inventory report
python -m projects.net_discovery.src.scanner --target 192.168.1.0/24

# Docker Compose generator — web or monitoring stacks
python -m projects.docker_stacks.src.compose --stack web

# Monitor agent — system health (CPU, memory, disk, alert)
python -m projects.monitor_agent.src.agent

# Storage health — disk usage, SMART, IOPS, latency
python -m projects.storage_health.src.checker

# IaC templates — cloud-init or Docker Compose setup
python -m projects.iac_scripts.src.templates --template cloud-init

# Secrets manager — AES-256 encrypted vault (Fernet + PBKDF2)
python -m projects.vault_secrets.src.vault --help
```
