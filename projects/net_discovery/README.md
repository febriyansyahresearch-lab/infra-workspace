# Network Discovery — Ping Sweep, Port Scan, Inventory

**Use Case:** Presales network assessment demo  
**Techniques:** TCP ping, port scanning, inventory reporting

## Features
- Ping sweep across subnet (CIDR)
- Multi-threaded port scan
- Network inventory report generation

## Usage
```bash
python -m projects.net_discovery.src.scanner 192.168.1.0/24
python -m projects.net_discovery.src.scanner 10.0.0.1 --ports 22 80 443 --inventory
```
