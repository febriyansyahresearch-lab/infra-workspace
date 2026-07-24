import time
import json
import platform
from datetime import datetime
from typing import Optional


def get_cpu_percent() -> float:
    import psutil
    return psutil.cpu_percent(interval=0.5)


def get_memory_info() -> dict:
    import psutil
    mem = psutil.virtual_memory()
    return {"total_gb": round(mem.total / (1024 ** 3), 2), "used_gb": round(mem.used / (1024 ** 3), 2), "percent": mem.percent}


def get_disk_info(path: str = "/") -> dict:
    import psutil
    disk = psutil.disk_usage(path)
    return {"mount": path, "total_gb": round(disk.total / (1024 ** 3), 2), "used_gb": round(disk.used / (1024 ** 3), 2), "percent": disk.percent}


def get_uptime() -> str:
    import psutil
    boot = datetime.fromtimestamp(psutil.boot_time())
    return str(datetime.now() - boot).split(".")[0]


def check_health(cpu_threshold: float = 80.0, mem_threshold: float = 80.0, disk_threshold: float = 90.0) -> dict:
    cpu = get_cpu_percent()
    mem = get_memory_info()
    disk = get_disk_info()
    alerts = []

    if cpu > cpu_threshold:
        alerts.append(f"CPU high: {cpu}% > {cpu_threshold}%")
    if mem["percent"] > mem_threshold:
        alerts.append(f"Memory high: {mem['percent']}% > {mem_threshold}%")
    if disk["percent"] > disk_threshold:
        alerts.append(f"Disk high: {disk['percent']}% > {disk_threshold}%")

    return {
        "timestamp": datetime.now().isoformat(),
        "hostname": platform.node(),
        "cpu_percent": cpu,
        "memory": mem,
        "disk": disk,
        "uptime": get_uptime(),
        "status": "ALERT" if alerts else "HEALTHY",
        "alerts": alerts,
    }


def simulate_metrics() -> dict:
    import numpy as np
    return {
        "timestamp": datetime.now().isoformat(),
        "cpu_percent": round(float(np.clip(np.random.default_rng().normal(45, 15), 0, 100)), 1),
        "memory_percent": round(float(np.clip(np.random.default_rng().normal(55, 10), 0, 100)), 1),
        "disk_percent": round(float(np.clip(np.random.default_rng().normal(40, 20), 0, 100)), 1),
        "uptime": "2 days, 5:30:00",
        "status": "HEALTHY",
        "alerts": [],
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="System health checker")
    parser.add_argument("--simulate", action="store_true", help="Use simulated metrics (no psutil)")
    args = parser.parse_args()
    result = simulate_metrics() if args.simulate else check_health()
    print(json.dumps(result, indent=2))
