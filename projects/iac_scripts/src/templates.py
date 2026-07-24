import json
import yaml


CLOUD_INIT_TEMPLATE = """#cloud-config
package_update: true
packages:
  - nginx
  - docker.io
  - docker-compose
write_files:
  - path: /etc/nginx/sites-available/default
    content: |
      server {{
          listen 80;
          server_name {domain};
          location / {{ proxy_pass http://127.0.0.1:8000; }}
      }}
runcmd:
  - systemctl enable nginx && systemctl start nginx
  - systemctl enable docker && systemctl start docker
"""


DOCKER_COMPOSE_APP = """version: '3.8'
services:
  app:
    image: nginx:alpine
    ports:
      - "8000:80"
  redis:
    image: redis:alpine
"""


def generate_cloud_init(domain: str = "demo.local") -> str:
    return CLOUD_INIT_TEMPLATE.format(domain=domain)


def generate_docker_compose(app_name: str = "app", port: int = 8000) -> str:
    return yaml.dump({
        "version": "3.8",
        "services": {
            app_name: {
                "image": "nginx:alpine",
                "ports": [f"{port}:80"],
            },
        },
    }, default_flow_style=False)


def list_templates() -> list[dict]:
    return [
        {"name": "cloud-init-web", "desc": "Cloud-init for web server with nginx + docker", "type": "cloud-init"},
        {"name": "docker-compose-app", "desc": "Minimal Docker Compose for app service", "type": "docker-compose"},
    ]


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="IaC template generator")
    parser.add_argument("template", choices=["cloud-init", "compose", "list"])
    args = parser.parse_args()
    if args.template == "list":
        for t in list_templates():
            print(f"{t['name']}: {t['desc']}")
    elif args.template == "cloud-init":
        print(generate_cloud_init())
    else:
        print(generate_docker_compose())
