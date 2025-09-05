#!/usr/bin/env python3
"""
Builds a topology JSON (like in your screenshots) from 3 CSVs:
  nodes.csv, interfaces.csv, networks.csv

Usage:
  python generate_topology.py \
    --schema https://portal.mipn.co.uk/topologyschema-01/schema# \
    --nodes nodes.csv --interfaces interfaces.csv --networks networks.csv \
    --out topology.json
"""

import csv, json, argparse
from collections import defaultdict

def parse_tags(s):
    if not s:
        return []
    return [t.strip() for t in s.split(';') if t.strip()]

def maybe_int(v):
    if v is None:
        return None
    v = str(v).strip()
    if v == '':
        return None
    try:
        return int(v)
    except ValueError:
        return None

def read_nodes(path):
    nodes = []
    auto_id = 1
    with open(path, newline='') as f:
        rdr = csv.DictReader(f)
        for row in rdr:
            node_id = maybe_int(row.get('id')) or auto_id
            if maybe_int(row.get('id')) is None:
                auto_id += 1
            name = row.get('name','').strip()
            typ = row.get('type','').strip()
            templateName = (row.get('templateName') or '').strip() or None
            osType = (row.get('osType') or '').strip() or None
            tags = parse_tags(row.get('tags',''))
            description = (row.get('description') or '').strip() or None

            n = {"id": node_id, "name": name, "type": typ, "interfaces": []}
            if description:
                n["description"] = description
            cfg = {}
            if templateName: cfg["templateName"] = templateName
            if osType: cfg["osType"] = osType
            if tags: cfg["tags"] = tags
            if cfg:
                n["config"] = cfg
            nodes.append(n)
    return nodes

def read_networks(path):
    nets = []
    with open(path, newline='') as f:
        rdr = csv.DictReader(f)
        for row in rdr:
            net = {
                "type": (row.get("type") or "unmanaged").strip(),
                "name": (row.get("name") or "").strip(),
            }
            net_id = maybe_int(row.get("id"))
            if net_id is not None:
                net["id"] = net_id

            maxbw = maybe_int(row.get("maximumBandwidth"))
            if maxbw is not None:
                net["maximumBandwidth"] = maxbw

            defaults = {}
            for k in ["bandwidth","latency","jitter","loss","corruption","mtu"]:
                m = maybe_int(row.get(f"defaults.{k}"))
                if m is not None:
                    defaults[k] = m
            if defaults:
                net["defaults"] = defaults

            nets.append(net)
    return nets

def read_interfaces(path):
    ifaces = []
    with open(path, newline='') as f:
        rdr = csv.DictReader(f)
        for row in rdr:
            iface = {}
            node_id = maybe_int(row.get("node_id"))
            node_name = (row.get("node_name") or "").strip() or None
            if node_id is not None:
                iface["_node_id"] = node_id
            elif node_name:
                iface["_node_name"] = node_name

            iface["name"] = (row.get("name") or "").strip()
            nid = maybe_int(row.get("networkId"))
            if nid is not None:
                iface["networkId"] = nid
            ipv4 = (row.get("ipv4Addr") or "").strip()
            mac = (row.get("macAddr") or "").strip()
            if ipv4: iface["ipv4Addr"] = ipv4
            if mac: iface["macAddr"] = mac
            ifaces.append(iface)
    return ifaces

def attach_interfaces(nodes, ifaces):
    by_id = {n["id"]: n for n in nodes}
    by_name = {n["name"]: n for n in nodes}
    for iface in ifaces:
        tgt = None
        if "_node_id" in iface:
            tgt = by_id.get(iface["_node_id"])
        elif "_node_name" in iface:
            tgt = by_name.get(iface["_node_name"])
        if tgt is None:
            raise ValueError(f"Interface refers to unknown node: {iface}")
        clean = {k:v for k,v in iface.items() if not k.startswith('_')}
        tgt["interfaces"].append(clean)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--schema", default="https://portal.mipn.co.uk/topologyschema-01/schema#")
    ap.add_argument("--nodes", required=True)
    ap.add_argument("--interfaces", required=True)
    ap.add_argument("--networks", required=True)
    ap.add_argument("--out", default="topology.json")
    args = ap.parse_args()

    nodes = read_nodes(args.nodes)
    ifaces = read_interfaces(args.interfaces)
    attach_interfaces(nodes, ifaces)
    networks = read_networks(args.networks)

    topo = {"$schema": args.schema, "nodes": nodes, "networks": networks}
    with open(args.out, "w") as f:
        json.dump(topo, f, indent=2)
    print(f"Wrote {args.out}")

if __name__ == "__main__":
    main()
