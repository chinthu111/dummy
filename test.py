#!/usr/bin/env python3
"""
json_to_csv.py

Reads topology.json and regenerates nodes.csv, interfaces.csv, and networks.csv.

Usage:
    python json_to_csv.py --topology topology.json --outdir regenerated_csvs
"""

import json
import argparse
import csv
import os

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--topology", required=True, help="Input topology.json file")
    ap.add_argument("--outdir", default="regenerated_csvs", help="Output directory for CSVs")
    args = ap.parse_args()

    with open(args.topology) as f:
        topo = json.load(f)

    os.makedirs(args.outdir, exist_ok=True)

    # --- Write nodes.csv ---
    with open(os.path.join(args.outdir, "nodes.csv"), "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "name", "type"])
        writer.writeheader()
        for node in topo.get("nodes", []):
            writer.writerow({
                "id": node.get("id"),
                "name": node.get("name"),
                "type": node.get("type"),
            })

    # --- Write interfaces.csv ---
    with open(os.path.join(args.outdir, "interfaces.csv"), "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["node_id", "name", "networkId"])
        writer.writeheader()
        for node in topo.get("nodes", []):
            for iface in node.get("interfaces", []):
                writer.writerow({
                    "node_id": node.get("id"),
                    "name": iface.get("name"),
                    "networkId": iface.get("networkId"),
                })

    # --- Write networks.csv ---
    with open(os.path.join(args.outdir, "networks.csv"), "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "name", "type"])
        writer.writeheader()
        for net in topo.get("networks", []):
            writer.writerow({
                "id": net.get("id"),
                "name": net.get("name"),
                "type": net.get("type"),
            })

    print(f"Regenerated CSVs saved in {args.outdir}/")

if __name__ == "__main__":
    main()
