import pytest
from projects.net_discovery.src.scanner import scan_port, COMMON_PORTS, generate_inventory, discover_network


def test_scan_port_returns_dict_or_none():
    result = scan_port("127.0.0.1", 9999, timeout=0.3)
    assert result is None or isinstance(result, dict)


def test_common_ports_defined():
    assert 22 in COMMON_PORTS
    assert 80 in COMMON_PORTS
    assert 443 in COMMON_PORTS


def test_generate_inventory_format():
    hosts = [{"ip": "10.0.0.1", "open_ports": [{"port": 22, "service": "SSH", "state": "open"}]}]
    report = generate_inventory(hosts)
    assert "[10.0.0.1]" in report
    assert "SSH" in report
