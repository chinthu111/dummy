#!/usr/bin/env python3
import json, csv, argparse, os

NODE_HEADERS = ["id","name","type","templateName","osType","tags","description"]
IFACE_HEADERS = ["node_id","node_name","name","networkId","ipv4Addr","macAddr"]
NET_HEADERS = ["id","name","type","maximumBandwidth",
               "defaults.bandwidth","defaults.latency","defaults.jitter",
               "defaults.loss","defaults.corruption","defaults.mtu"]

def write_nodes(nodes, outpath):
    with open(outpath, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=NODE_HEADERS)
        w.writeheader()
        for n in nodes:
            cfg = n.get("config", {}) or {}
            tags = cfg.get("tags") or []
            tags_str = ";".join(tags) if isinstance(tags, list) else (tags or "")
            row = {
                "id": n.get("id",""),
                "name": n.get("name",""),
                "type": n.get("type",""),
                "templateName": cfg.get("templateName",""),
                "osType": cfg.get("osType",""),
                "tags": tags_str,
                "description": n.get("description","") or "",
            }
            w.writerow(row)

def write_interfaces(nodes, outpath):
    with open(outpath, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=IFACE_HEADERS)
        w.writeheader()
        for n in nodes:
            node_id = n.get("id","")
            node_name = n.get("name","")
            for iface in n.get("interfaces", []) or []:
                row = {
                    "node_id": node_id,
                    "node_name": node_name,
                    "name": iface.get("name",""),
                    "networkId": iface.get("networkId",""),
                    "ipv4Addr": iface.get("ipv4Addr",""),
                    "macAddr": iface.get("macAddr",""),
                }
                w.writerow(row)

def write_networks(networks, outpath):
    with open(outpath, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=NET_HEADERS)
        w.writeheader()
        for net in networks:
            defaults = net.get("defaults", {}) or {}
            row = {
                "id": net.get("id",""),
                "name": net.get("name",""),
                "type": net.get("type",""),
                "maximumBandwidth": net.get("maximumBandwidth",""),
                "defaults.bandwidth": defaults.get("bandwidth",""),
                "defaults.latency": defaults.get("latency",""),
                "defaults.jitter": defaults.get("jitter",""),
                "defaults.loss": defaults.get("loss",""),
                "defaults.corruption": defaults.get("corruption",""),
                "defaults.mtu": defaults.get("mtu",""),
            }
            w.writerow(row)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--topology", required=True, help="Input topology.json")
    ap.add_argument("--outdir", default="regenerated_csvs_full", help="Output directory")
    args = ap.parse_args()

    with open(args.topology) as f:
        topo = json.load(f)

    os.makedirs(args.outdir, exist_ok=True)

    nodes = topo.get("nodes", []) or []
    networks = topo.get("networks", []) or []

    write_nodes(nodes, os.path.join(args.outdir, "nodes.csv"))
    write_interfaces(nodes, os.path.join(args.outdir, "interfaces.csv"))
    write_networks(networks, os.path.join(args.outdir, "networks.csv"))

    print(f"Wrote regenerated CSVs to {args.outdir}")

if __name__ == "__main__":
    main()
