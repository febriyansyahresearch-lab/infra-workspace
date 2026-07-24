.PHONY: setup test scan-net generate-compose run-agent check-storage generate-iac vault lint clean

setup:
	pip install -r requirements.txt

test:
	python -m pytest projects/ -v

scan-net:
	python -m projects.net_discovery.src.scanner --target 192.168.1.0/24

generate-compose:
	python -m projects.docker_stacks.src.compose --stack web

run-agent:
	python -m projects.monitor_agent.src.agent

check-storage:
	python -m projects.storage_health.src.checker

generate-iac:
	python -m projects.iac_scripts.src.templates --template cloud-init

vault:
	python -m projects.vault_secrets.src.vault --help

lint:
	ruff check . --ignore E501 || true

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
