import json
import platform
from datetime import datetime
from typing import Optional


def parse_df_output() -> list[dict]:
    import subprocess
    import re
    try:
        result = subprocess.run(["df", "-h"], capture_output=True, text=True, timeout=5)
        lines = result.stdout.strip().split("\n")[1:]
        mounts = []
        for line in lines:
            parts = line.split()
            if len(parts) >= 6:
                mounts.append({
                    "filesystem": parts[0], "size": parts[1], "used": parts[2],
                    "avail": parts[3], "use_percent": parts[4].replace("%", ""),
                    "mount": parts[5],
                })
        return mounts
    except Exception:
        return []


def simulate_disk_info() -> list[dict]:
    import numpy as np
    rng = np.random.default_rng(42)
    mounts = [
        {"fs": "/dev/sda1", "mount": "/", "size_gb": 100, "used_gb": round(float(rng.uniform(30, 80)), 1), "type": "ext4"},
        {"fs": "/dev/sdb1", "mount": "/data", "size_gb": 500, "used_gb": round(float(rng.uniform(100, 400)), 1), "type": "xfs"},
        {"fs": "/dev/sdc1", "mount": "/backup", "size_gb": 1000, "used_gb": round(float(rng.uniform(200, 600)), 1), "type": "ext4"},
    ]
    for m in mounts:
        m["use_percent"] = round(m["used_gb"] / m["size_gb"] * 100, 1)
    return mounts


def simulate_smart_data() -> dict:
    return {
        "device": "/dev/sda",
        "model": "SSD-DATA-1TB",
        "temperature_c": 42,
        "power_on_hours": 8760,
        "reallocated_sectors": 0,
        "pending_sectors": 0,
        "status": "PASSED",
    }


def simulate_iops() -> dict:
    import numpy as np
    rng = np.random.default_rng(42)
    return {
        "read_iops": int(rng.poisson(2500)),
        "write_iops": int(rng.poisson(1800)),
        "read_latency_ms": round(float(rng.exponential(5)), 2),
        "write_latency_ms": round(float(rng.exponential(8)), 2),
    }


def health_report(threshold: float = 85.0) -> dict:
    disks = simulate_disk_info()
    smart = simulate_smart_data()
    iops = simulate_iops()
    alerts = []

    for d in disks:
        if d["use_percent"] > threshold:
            alerts.append(f"Disk {d['mount']} at {d['use_percent']}% capacity")

    return {
        "timestamp": datetime.now().isoformat(),
        "host": platform.node(),
        "disks": disks,
        "smart": smart,
        "iops": iops,
        "status": "ALERT" if alerts else "HEALTHY",
        "alerts": alerts,
    }


if __name__ == "__main__":
    result = health_report()
    print(json.dumps(result, indent=2))
