#!/usr/bin/env python3
"""
validate_topology_csvs.py

Validates nodes.csv, interfaces.csv, and networks.csv before generating topology.json.

Checks performed:
1. Structural validation:
   - Required columns exist
   - No empty mandatory fields
2. Cross-reference validation:
   - Interfaces reference valid node_id or node_name
   - Interfaces reference valid networkId
3. Duplicate detection:
   - Node IDs must be unique
   - Node names should be unique (warning if duplicates)
   - Network IDs must be unique
   - Interface names must be unique per node
4. Format checks:
   - IDs, networkIds must be integers
   - ipv4Addr in CIDR format
   - macAddr in XX:XX:XX:XX:XX:XX format

Usage:
    python validate_topology_csvs.py --nodes nodes.csv --interfaces interfaces.csv --networks networks.csv
"""

import argparse, csv, re, ipaddress
from collections import defaultdict, Counter

def read_csv(path):
    with open(path, newline='') as f:
        return list(csv.DictReader(f))

def validate_nodes(rows, errors, warnings):
    seen_ids = set()
    seen_names = Counter()
    for i, row in enumerate(rows, start=2):  # header is row 1
        rid = row.get("id", "").strip()
        name = row.get("name", "").strip()
        typ = row.get("type", "").strip()

        # Required fields
        if not name:
            errors.append(f"nodes.csv line {i}: Missing name")
        if not typ:
            errors.append(f"nodes.csv line {i}: Missing type")

        # ID checks
        if rid:
            try:
                rid_int = int(rid)
                if rid_int in seen_ids:
                    errors.append(f"nodes.csv line {i}: Duplicate node id {rid_int}")
                seen_ids.add(rid_int)
            except ValueError:
                errors.append(f"nodes.csv line {i}: Invalid id '{rid}' (must be integer)")
        seen_names[name] += 1

    # Warn if duplicate names
    for n, count in seen_names.items():
        if count > 1:
            warnings.append(f"nodes.csv: Duplicate node name '{n}' appears {count} times")

    return seen_ids, set(seen_names.keys())

def validate_networks(rows, errors, warnings):
    seen_ids = set()
    seen_names = Counter()
    for i, row in enumerate(rows, start=2):
        rid = row.get("id", "").strip()
        name = row.get("name", "").strip()
        if not rid:
            errors.append(f"networks.csv line {i}: Missing id")
        else:
            try:
                rid_int = int(rid)
                if rid_int in seen_ids:
                    errors.append(f"networks.csv line {i}: Duplicate network id {rid_int}")
                seen_ids.add(rid_int)
            except ValueError:
                errors.append(f"networks.csv line {i}: Invalid id '{rid}' (must be integer)")
        if not name:
            errors.append(f"networks.csv line {i}: Missing name")
        seen_names[name] += 1

    # Warn if duplicate names
    for n, count in seen_names.items():
        if count > 1:
            warnings.append(f"networks.csv: Duplicate network name '{n}' appears {count} times")

    return seen_ids

def validate_interfaces(rows, node_ids, node_names, network_ids, errors, warnings):
    iface_keys = set()
    for i, row in enumerate(rows, start=2):
        nid = row.get("node_id", "").strip()
        nname = row.get("node_name", "").strip()
        iface_name = row.get("name", "").strip()
        netid = row.get("networkId", "").strip()
        ip = row.get("ipv4Addr", "").strip()
        mac = row.get("macAddr", "").strip()

        # Node check
        node_ref = None
        if nid:
            try:
                nid_int = int(nid)
                if nid_int not in node_ids:
                    errors.append(f"interfaces.csv line {i}: node_id {nid_int} not found in nodes.csv")
                node_ref = f"id:{nid_int}"
            except ValueError:
                errors.append(f"interfaces.csv line {i}: Invalid node_id '{nid}'")
        elif nname:
            if nname not in node_names:
                errors.append(f"interfaces.csv line {i}: node_name '{nname}' not found in nodes.csv")
            node_ref = f"name:{nname}"
        else:
            errors.append(f"interfaces.csv line {i}: Missing both node_id and node_name")

        # Interface name
        if not iface_name:
            errors.append(f"interfaces.csv line {i}: Missing interface name")

        # Network check
        if not netid:
            errors.append(f"interfaces.csv line {i}: Missing networkId")
        else:
            try:
                netid_int = int(netid)
                if netid_int not in network_ids:
                    errors.append(f"interfaces.csv line {i}: networkId {netid_int} not found in networks.csv")
            except ValueError:
                errors.append(f"interfaces.csv line {i}: Invalid networkId '{netid}'")

        # Duplicate interface name per node
        if node_ref and iface_name:
            key = (node_ref, iface_name)
            if key in iface_keys:
                errors.append(f"interfaces.csv line {i}: Duplicate interface '{iface_name}' for {node_ref}")
            iface_keys.add(key)

        # IP format check
        if ip:
            try:
                ipaddress.ip_network(ip, strict=False)
            except ValueError:
                errors.append(f"interfaces.csv line {i}: Invalid ipv4Addr '{ip}' (must be CIDR)")

        # MAC format check
        if mac:
            if not re.match(r"^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$", mac):
                errors.append(f"interfaces.csv line {i}: Invalid macAddr '{mac}'")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nodes", required=True)
    ap.add_argument("--interfaces", required=True)
    ap.add_argument("--networks", required=True)
    args = ap.parse_args()

    errors, warnings = [], []

    nodes = read_csv(args.nodes)
    networks = read_csv(args.networks)
    interfaces = read_csv(args.interfaces)

    node_ids, node_names = validate_nodes(nodes, errors, warnings)
    network_ids = validate_networks(networks, errors, warnings)
    validate_interfaces(interfaces, node_ids, node_names, network_ids, errors, warnings)

    print("Validation Results:")
    if errors:
        print("\nErrors:")
        for e in errors:
            print("  -", e)
    if warnings:
        print("\nWarnings:")
        for w in warnings:
            print("  -", w)
    if not errors and not warnings:
        print("  All good ✅")

    if errors:
        exit(1)  # fail if errors

if __name__ == "__main__":
    main()
