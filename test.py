#!/usr/bin/env python3
"""
topology_relationships.py

Reads topology.json and outputs node->interface->network relationships.

Usage:
    python topology_relationships.py --topology topology.json --out topology_report.txt
"""

import json
import argparse
from collections import defaultdict

def generate_report(topology):
    nodes = topology.get("nodes", [])
    networks = {net["id"]: net for net in topology.get("networks", [])}
    net_to_ifaces = defaultdict(list)

    lines = []
    lines.append("=== Node View ===\n")
    for node in nodes:
        lines.append(f"Node: {node.get('name')} (id={node.get('id')}, type={node.get('type')})")
        for iface in node.get("interfaces", []):
            netid = iface.get("networkId")
            netname = networks.get(netid, {}).get("name", f"UNKNOWN({netid})")
            lines.append(f"  - Interface {iface.get('name')} -> Network {netname} (id={netid})")
            net_to_ifaces[netid].append((node.get("name"), iface.get("name")))
        lines.append("")

    lines.append("\n=== Network View ===\n")
    for netid, net in networks.items():
        lines.append(f"Network: {net.get('name')} (id={netid}, type={net.get('type')})")
        attached = net_to_ifaces.get(netid, [])
        if not attached:
            lines.append("  - No nodes connected")
        else:
            for nodename, ifname in attached:
                lines.append(f"  - {nodename} via {ifname}")
        lines.append("")

    return "\n".join(lines)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--topology", required=True, help="Input topology.json file")
    ap.add_argument("--out", default="topology_report.txt", help="Output report file")
    args = ap.parse_args()

    with open(args.topology) as f:
        topo = json.load(f)

    report = generate_report(topo)

    with open(args.out, "w") as f:
        f.write(report)

    print(f"Topology relationship report written to {args.out}")

if __name__ == "__main__":
    main()
