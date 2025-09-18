#!/usr/bin/env python3
import json, csv, argparse, os

# Full schema headers (fixed mode)
NODE_HEADERS = ["id","name","type","templateName","osType","tags","description"]
IFACE_HEADERS = ["node_id","node_name","name","networkId","ipv4Addr","macAddr"]
NET_HEADERS   = ["id","name","type","maximumBandwidth",
                 "defaults.bandwidth","defaults.latency","defaults.jitter",
                 "defaults.loss","defaults.corruption","defaults.mtu"]

def to_rows_nodes(nodes):
    rows = []
    for n in nodes:
        cfg = n.get("config") or {}
        tags = cfg.get("tags") or []
        rows.append({
            "id": n.get("id",""),
            "name": n.get("name",""),
            "type": n.get("type",""),
            "templateName": cfg.get("templateName","") or "",
            "osType": cfg.get("osType","") or "",
            "tags": ";".join(tags) if isinstance(tags, list) else (tags or ""),
            "description": n.get("description","") or "",
        })
    return rows

def to_rows_ifaces(nodes, include_node_name=True):
    rows = []
    for n in nodes:
        node_id = n.get("id","")
        node_name = n.get("name","")
        for iface in n.get("interfaces") or []:
            row = {
                "node_id": node_id,
                "node_name": node_name if include_node_name else "",
                "name": iface.get("name","") or "",
                "networkId": iface.get("networkId","") or "",
                "ipv4Addr": iface.get("ipv4Addr","") or "",
                "macAddr": iface.get("macAddr","") or "",
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
            "id": net.get("id",""),
            "name": net.get("name","") or "",
            "type": net.get("type","") or "",
            "maximumBandwidth": net.get("maximumBandwidth","") or "",
            "defaults.bandwidth": d.get("bandwidth","") or "",
            "defaults.latency": d.get("latency","") or "",
            "defaults.jitter": d.get("jitter","") or "",
            "defaults.loss": d.get("loss","") or "",
            "defaults.corruption": d.get("corruption","") or "",
            "defaults.mtu": d.get("mtu","") or "",
        })
    return rows

def trim_trailing_empty_columns(headers, rows):
    """
    Compact mode:
    - Find the last column index that has a non-empty value in ANY row.
    - Return trimmed headers and rows up to that column.
    """
    if not rows:
        return headers, rows
    last_idx = -1
    for i, h in enumerate(headers):
        has_nonempty = any((str(r.get(h, "")).strip() != "") for r in rows)
        if has_nonempty:
            last_idx = i
    if last_idx == -1:
        # everything empty; keep first column to avoid empty CSVs
        last_idx = 0
    trimmed_headers = headers[:last_idx+1]
    trimmed_rows = [{h: r.get(h, "") for h in trimmed_headers} for r in rows]
    return trimmed_headers, trimmed_rows

def write_csv(path, headers, rows):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=headers)
        w.writeheader()
        for r in rows:
            w.writerow(r)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--topology", required=True, help="Input topology.json")
    ap.add_argument("--outdir", default="regenerated_csvs_full", help="Output dir")
    ap.add_argument("--style", choices=["fixed","compact"], default="fixed",
                    help="fixed = full schema columns; compact = trim trailing empty columns")
    ap.add_argument("--include-node-name", dest="include_node_name",
                    action="store_true", help="Include node_name column in interfaces (default)")
    ap.add_argument("--no-node-name", dest="include_node_name",
                    action="store_false", help="Exclude node_name column in interfaces")
    ap.set_defaults(include_node_name=True)
    args = ap.parse_args()

    with open(args.topology) as f:
        topo = json.load(f)

    os.makedirs(args.outdir, exist_ok=True)
    nodes = topo.get("nodes") or []
    networks = topo.get("networks") or []

    # Build row lists
    node_rows = to_rows_nodes(nodes)
    iface_rows = to_rows_ifaces(nodes, include_node_name=args.include_node_name)
    net_rows = to_rows_networks(networks)

    # Decide headers by style
    node_headers = NODE_HEADERS[:]
    iface_headers = (IFACE_HEADERS[:] if args.include_node_name
                     else [h for h in IFACE_HEADERS if h != "node_name"])
    net_headers = NET_HEADERS[:]

    if args.style == "compact":
        node_headers, node_rows = trim_trailing_empty_columns(node_headers, node_rows)
        iface_headers, iface_rows = trim_trailing_empty_columns(iface_headers, iface_rows)
        net_headers, net_rows = trim_trailing_empty_columns(net_headers, net_rows)

    # Write
    write_csv(os.path.join(args.outdir, "nodes.csv"), node_headers, node_rows)
    write_csv(os.path.join(args.outdir, "interfaces.csv"), iface_headers, iface_rows)
    write_csv(os.path.join(args.outdir, "networks.csv"), net_headers, net_rows)

    print(f"CSV files written to {args.outdir}/")
    print(f"Style: {args.style}, include_node_name: {args.include_node_name}")

if __name__ == "__main__":
    main()
