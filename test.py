#!/usr/bin/env python3
"""
draw_topology.py

Reads topology.json and outputs a Mermaid diagram file (topology.mmd).

Usage:
    python draw_topology.py --topology topology.json --out topology.mmd
"""

import json
import argparse

def build_mermaid(topology):
    lines = ["graph TD"]

    # Index nodes by id for quick lookup
    nodes_by_id = {node["id"]: node for node in topology.get("nodes", [])}
    networks_by_id = {net["id"]: net for net in topology.get("networks", [])}

    # Add network nodes (special shape for clarity)
    for net in topology.get("networks", []):
        nid = net["id"]
        name = net.get("name", f"net{nid}")
        lines.append(f'  net{nid}(["{name}"])')

    # Add edges node -> network
    for node in topology.get("nodes", []):
        node_label = node.get("name", f'node{node["id"]}')
        lines.append(f'  node{node["id"]}["{node_label}"]')

        for iface in node.get("interfaces", []):
            netid = iface.get("networkId")
            if netid is None or netid not in networks_by_id:
                continue
            iface_label = iface.get("name", "")
            lines.append(f'  node{node["id"]} -- "{iface_label}" --> net{netid}')

    return "\n".join(lines)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--topology", required=True, help="Input topology.json file")
    ap.add_argument("--out", default="topology.mmd", help="Output Mermaid file")
    args = ap.parse_args()

    with open(args.topology) as f:
        topo = json.load(f)

    mermaid = build_mermaid(topo)

    with open(args.out, "w") as f:
        f.write(mermaid)

    print(f"Mermaid diagram saved to {args.out}")
    print("Preview with GitLab/GitHub markdown, or convert using mermaid-cli (mmdc).")

if __name__ == "__main__":
    main()
