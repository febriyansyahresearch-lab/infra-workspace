import pytest
from projects.iac_scripts.src.templates import generate_cloud_init, generate_docker_compose, list_templates


def test_generate_cloud_init():
    result = generate_cloud_init("test.local")
    assert "#cloud-config" in result
    assert "test.local" in result


def test_generate_docker_compose():
    result = generate_docker_compose("test-app", 8080)
    assert "test-app" in result
    assert "8080:80" in result


def test_list_templates():
    templates = list_templates()
    assert len(templates) >= 2
