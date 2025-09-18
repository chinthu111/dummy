#!/usr/bin/env python3
import json, csv, argparse, os

NODE_HEADERS = ["id","name","type","templateName","osType","tags","description"]
IFACE_HEADERS = ["node_id","node_name","name","networkId","ipv4Addr","macAddr"]
NET_HEADERS   = ["id","name","type","maximumBandwidth",
                 "defaults.bandwidth","defaults.latency","defaults.jitter",
                 "defaults.loss","defaults.corruption","defaults.mtu"]

def safe_val(v):
    """Return '' if None, else string value."""
    if v is None:
        return ""
    return str(v)

def to_rows_nodes(nodes):
    rows = []
    for n in nodes:
        cfg = n.get("config") or {}
        tags = cfg.get("tags") or []
        rows.append({
            "id": safe_val(n.get("id")),
            "name": safe_val(n.get("name")),
            "type": safe_val(n.get("type")),
            "templateName": safe_val(cfg.get("templateName")),
            "osType": safe_val(cfg.get("osType")),
            "tags": ";".join(tags) if isinstance(tags, list) else safe_val(tags),
            "description": safe_val(n.get("description")),
        })
    return rows

def to_rows_ifaces(nodes, include_node_name=True):
    rows = []
    for n in nodes:
        node_id = safe_val(n.get("id"))
        node_name = safe_val(n.get("name")) if include_node_name else ""
        for iface in n.get("interfaces") or []:
            row = {
                "node_id": node_id,
                "node_name": node_name if include_node_name else "",
                "name": safe_val(iface.get("name")),
                "networkId": safe_val(iface.get("networkId")),
                "ipv4Addr": safe_val(iface.get("ipv4Addr")),
                "macAddr": safe_val(iface.get("macAddr")),
            }
            if not include_node_name:
                del row["node_name"]
            rows.append(row)
    return rows

def to_rows_networks(networks):
    rows = []
    for net in networks:
        d = net.get("defaults") or {}
        rows.append({
            "id": safe_val(net.get("id")),
            "name": safe_val(net.get("name")),
            "type": safe_val(net.get("type")),
            "maximumBandwidth": safe_val(net.get("maximumBandwidth")),
            "defaults.bandwidth": safe_val(d.get("bandwidth")),
            "defaults.latency": safe_val(d.get("latency")),
            "defaults.jitter": safe_val(d.get("jitter")),
            "defaults.loss": safe_val(d.get("loss")),
            "defaults.corruption": safe_val(d.get("corruption")),
            "defaults.mtu": safe_val(d.get("mtu")),
        })
    return rows

def write_csv(path, headers, rows):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=headers, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({h: r.get(h, "") for h in headers})

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--topology", required=True, help="Input topology.json")
    ap.add_argument("--outdir", default="regenerated_csvs_full", help="Output dir")
    ap.add_argument("--no-node-name", dest="include_node_name",
                    action="store_false", help="Exclude node_name column in interfaces")
    ap.set_defaults(include_node_name=True)
    args = ap.parse_args()

    with open(args.topology) as f:
        topo = json.load(f)

    os.makedirs(args.outdir, exist_ok=True)
    nodes = topo.get("nodes") or []
    networks = topo.get("networks") or []

    node_rows = to_rows_nodes(nodes)
    iface_rows = to_rows_ifaces(nodes, include_node_name=args.include_node_name)
    net_rows = to_rows_networks(networks)

    node_headers = NODE_HEADERS[:]
    iface_headers = IFACE_HEADERS[:] if args.include_node_name else [h for h in IFACE_HEADERS if h != "node_name"]
    net_headers = NET_HEADERS[:]

    write_csv(os.path.join(args.outdir, "nodes.csv"), node_headers, node_rows)
    write_csv(os.path.join(args.outdir, "interfaces.csv"), iface_headers, iface_rows)
    write_csv(os.path.join(args.outdir, "networks.csv"), net_headers, net_rows)

    print(f"CSV files written to {args.outdir}/")

if __name__ == "__main__":
    main()
