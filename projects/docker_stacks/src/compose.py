import yaml
import json


def generate_web_stack(domain: str = "example.local") -> str:
    return yaml.dump({
        "version": "3.8",
        "services": {
            "nginx": {
                "image": "nginx:alpine",
                "ports": ["80:80", "443:443"],
                "volumes": ["./nginx/conf.d:/etc/nginx/conf.d"],
                "depends_on": ["app"],
            },
            "app": {
                "build": ".",
                "ports": ["8000:8000"],
                "environment": [f"DOMAIN={domain}", "DB_HOST=db"],
                "depends_on": ["db"],
            },
            "db": {
                "image": "postgres:15-alpine",
                "environment": ["POSTGRES_DB=appdb", "POSTGRES_USER=app", "POSTGRES_PASSWORD=changeme"],
                "volumes": ["pgdata:/var/lib/postgresql/data"],
            },
        },
        "volumes": {"pgdata": {}},
    }, default_flow_style=False)


def generate_monitoring_stack() -> str:
    return yaml.dump({
        "version": "3.8",
        "services": {
            "prometheus": {
                "image": "prom/prometheus",
                "ports": ["9090:9090"],
                "volumes": ["./prometheus.yml:/etc/prometheus/prometheus.yml"],
            },
            "grafana": {
                "image": "grafana/grafana",
                "ports": ["3000:3000"],
                "environment": ["GF_SECURITY_ADMIN_PASSWORD=admin"],
                "depends_on": ["prometheus"],
            },
            "node-exporter": {
                "image": "prom/node-exporter",
                "ports": ["9100:9100"],
            },
        },
    }, default_flow_style=False)


def list_stacks() -> list[dict]:
    return [
        {"name": "web", "description": "Nginx + App + PostgreSQL", "services": 3},
        {"name": "monitoring", "description": "Prometheus + Grafana + Node Exporter", "services": 3},
    ]


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Docker Compose stack generator")
    parser.add_argument("stack", choices=["web", "monitoring", "list"], help="Stack to generate")
    args = parser.parse_args()
    if args.stack == "list":
        for s in list_stacks():
            print(f"{s['name']}: {s['description']} ({s['services']} services)")
    else:
        gen = generate_web_stack if args.stack == "web" else generate_monitoring_stack
        print(gen())
