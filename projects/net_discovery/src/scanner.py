import socket
import ipaddress
import concurrent.futures
from typing import Optional

COMMON_PORTS = {22: "SSH", 80: "HTTP", 443: "HTTPS", 3389: "RDP", 8080: "HTTP-Proxy"}


def ping_host(ip: str, timeout: float = 2.0) -> bool:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, 7))
        sock.close()
        return result == 0
    except Exception:
        return False


def scan_port(ip: str, port: int, timeout: float = 1.0) -> Optional[dict]:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))
        sock.close()
        if result == 0:
            return {"port": port, "service": COMMON_PORTS.get(port, "Unknown"), "state": "open"}
    except Exception:
        pass
    return None


def discover_network(subnet: str, ports: list[int] | None = None) -> dict:
    network = ipaddress.ip_network(subnet, strict=False)
    ports = ports or [22, 80, 443]
    live_hosts = []

    for ip in network.hosts():
        ip_str = str(ip)
        if ping_host(ip_str):
            open_ports = []
            for port in ports:
                result = scan_port(ip_str, port)
                if result:
                    open_ports.append(result)
            live_hosts.append({"ip": ip_str, "open_ports": open_ports})

    return {"subnet": subnet, "total_hosts": network.num_addresses, "live_hosts": live_hosts}


def scan_ports(target: str, ports: list[int] | None = None, concurrency: int = 50) -> list[dict]:
    ports = ports or list(COMMON_PORTS.keys())
    results = []

    def scan(p):
        return scan_port(target, p)

    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as ex:
        futures = {ex.submit(scan, p): p for p in ports}
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                results.append(result)

    results.sort(key=lambda x: x["port"])
    return results


def generate_inventory(hosts: list[dict]) -> str:
    lines = ["# Network Inventory Report", f"# Generated: {__import__('datetime').datetime.now()}", ""]
    for host in hosts:
        lines.append(f"[{host['ip']}]")
        for p in host.get("open_ports", []):
            lines.append(f"  port={p['port']} service={p['service']}")
        lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Network discovery & port scanner")
    parser.add_argument("target", help="IP address or subnet (CIDR)")
    parser.add_argument("--ports", nargs="*", type=int, default=[22, 80, 443, 3389])
    parser.add_argument("--inventory", action="store_true", help="Generate inventory report")
    args = parser.parse_args()

    if "/" in args.target:
        result = discover_network(args.target, args.ports)
        print(f"Discovered {len(result['live_hosts'])} live hosts in {args.target}")
    else:
        result = scan_ports(args.target, args.ports)
        for r in result:
            print(f"Port {r['port']}/{r['service']}: {r['state']}")
