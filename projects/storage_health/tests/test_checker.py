import pytest
from projects.storage_health.src.checker import (
    simulate_disk_info, simulate_smart_data, simulate_iops, health_report
)


def test_simulate_disk_info():
    disks = simulate_disk_info()
    assert len(disks) >= 2
    for d in disks:
        assert "use_percent" in d
        assert d["use_percent"] > 0


def test_simulate_smart_data():
    smart = simulate_smart_data()
    assert smart["status"] == "PASSED"
    assert "temperature_c" in smart


def test_simulate_iops():
    iops = simulate_iops()
    assert iops["read_iops"] > 0
    assert iops["write_iops"] > 0


def test_health_report_keys():
    report = health_report(threshold=90.0)
    assert "disks" in report
    assert "smart" in report
    assert "iops" in report
