# Docker Stacks — Compose Templates for Presales Demos

**Use Case:** Quick POC deployments  
**Stacks:** Web (Nginx + App + DB), Monitoring (Prometheus + Grafana)

## Usage
```bash
python -m projects.docker_stacks.src.compose web
python -m projects.docker_stacks.src.compose monitoring
python -m projects.docker_stacks.src.compose list
```
