import pytest
import yaml
from projects.docker_stacks.src.compose import generate_web_stack, generate_monitoring_stack, list_stacks


def test_generate_web_stack_valid_yaml():
    result = generate_web_stack()
    data = yaml.safe_load(result)
    assert "services" in data
    assert "nginx" in data["services"]


def test_generate_monitoring_stack_valid_yaml():
    result = generate_monitoring_stack()
    data = yaml.safe_load(result)
    assert "prometheus" in data["services"]


def test_list_stacks():
    stacks = list_stacks()
    assert len(stacks) >= 2
    assert stacks[0]["name"] == "web"
