#!/usr/bin/env python3
"""
topology_relationships.py

Reads topology.json and prints node -> interface -> network relationships.

Usage:
    python topology_relationships.py --topology topology.json
"""

import json
import argparse
from collections import defaultdict

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--topology", required=True, help="Input topology.json file")
    args = ap.parse_args()

    with open(args.topology) as f:
        topo = json.load(f)

    nodes = topo.get("nodes", [])
    networks = {net["id"]: net for net in topo.get("networks", [])}

    # Reverse mapping: network -> list of (node, interface)
    net_to_ifaces = defaultdict(list)

    print("\n=== Node View ===\n")
    for node in nodes:
        print(f"Node: {node.get('name')} (id={node.get('id')}, type={node.get('type')})")
        for iface in node.get("interfaces", []):
            netid = iface.get("networkId")
            netname = networks.get(netid, {}).get("name", f"UNKNOWN({netid})")
            print(f"  - Interface {iface.get('name')} -> Network {netname} (id={netid})")
            net_to_ifaces[netid].append((node.get("name"), iface.get("name")))
        print()

    print("\n=== Network View ===\n")
    for netid, net in networks.items():
        print(f"Network: {net.get('name')} (id={netid}, type={net.get('type')})")
        attached = net_to_ifaces.get(netid, [])
        if not attached:
            print("  - No nodes connected")
        else:
            for nodename, ifname in attached:
                print(f"  - {nodename} via {ifname}")
        print()

if __name__ == "__main__":
    main()
