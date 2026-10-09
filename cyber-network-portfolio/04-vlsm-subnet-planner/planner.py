"""Deterministic IPv4 VLSM planning; offline, no network commands."""
import argparse
import csv
import ipaddress
import json
from pathlib import Path


def allocate(parent_cidr, requests):
    base = ipaddress.ip_network(parent_cidr, strict=True)
    if base.version != 4:
        raise ValueError("IPv4 only")
    if not requests:
        raise ValueError("at least one segment is required")
    used_names = set()
    normalized = []
    for name, hosts in requests:
        name = name.strip()
        hosts = int(hosts)
        if not name or name in used_names:
            raise ValueError("duplicate or empty segment name")
        if hosts < 1:
            raise ValueError("host count must be positive")
        used_names.add(name)
        normalized.append((name, hosts))
    # Largest-first makes alignment predictable for decreasing subnet sizes.
    normalized.sort(key=lambda item: (-item[1], item[0]))
    pos = int(base.network_address)
    end = int(base.broadcast_address)
    plan = []
    for name, hosts in normalized:
        size_power = max(2, (hosts + 1).bit_length())
        size = 1 << size_power  # hosts + network + broadcast; /30 minimum
        if size > base.num_addresses:
            raise ValueError("requirements exceed available address space")
        aligned = (pos + size - 1) // size * size
        if aligned + size - 1 > end:
            raise ValueError("insufficient remaining address space")
        subnet = ipaddress.IPv4Network((aligned, 32 - size_power), strict=True)
        plan.append({
            "segment": name,
            "required_hosts": hosts,
            "subnet": str(subnet),
            "netmask": str(subnet.netmask),
            "gateway_suggestion": str(subnet.network_address + 1),
            "usable_hosts": size - 2,
            "first_usable": str(subnet.network_address + 1),
            "last_usable": str(subnet.broadcast_address - 1),
            "broadcast": str(subnet.broadcast_address),
            "spare_usable_hosts": size - 2 - hosts,
        })
        pos = aligned + size
    return plan


def read_requirements(path):
    with Path(path).open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames or not {"segment", "required_hosts"}.issubset(reader.fieldnames):
            raise ValueError("expected segment,required_hosts columns")
        return [(r["segment"], r["required_hosts"]) for r in reader]


def main():
    root = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description="Offline IPv4 VLSM subnet allocator")
    parser.add_argument("--base", default="192.168.50.0/24")
    parser.add_argument("--input", type=Path, default=root / "data/requirements.csv")
    parser.add_argument("--output", type=Path, default=root / "outputs/plan.csv")
    args = parser.parse_args()
    plan = allocate(args.base, read_requirements(args.input))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=plan[0].keys())
        writer.writeheader()
        writer.writerows(plan)
    (args.output.parent / "plan.json").write_text(
        json.dumps({"base": args.base, "allocations": plan}, indent=2) + "\n")
    for item in plan:
        print(f'{item["segment"]:20} {item["subnet"]:20} usable={item["usable_hosts"]}')


if __name__ == "__main__":
    main()
