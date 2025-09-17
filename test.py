import json
import sys
import itertools
import networkx as nx
import matplotlib.pyplot as plt

"""
Topology JSON shape expected:
{
  "devices": [
    { "id": "R1", "label": "Router R1", "interfaces": [ { "id": "R1-G0/0", "name": "G0/0" }, ... ] },
    ...
  ],
    "links": [
      { "a": { "device": "R1", "iface": "R1-G0/0" }, "b": { "device": "SW1", "iface": "SW1-G1/0/1" }, "bw": "1G", "status": "up" },
      ...
    ]
}
"""

def edge_label(link):
    a = f'{link["a"]["device"]}:{link["a"]["iface"]}'
    b = f'{link["b"]["device"]}:{link["b"]["iface"]}'
    extras = " • ".join([x for x in [link.get("bw"), link.get("status")] if x])
    return f"{a} ↔ {b}" + (f" • {extras}" if extras else "")

def main(path):
    with open(path) as f:
        topo = json.load(f)

    devices = {d["id"]: d for d in topo.get("devices", [])}
    iface_ids = { (d["id"], i["id"]) for d in topo.get("devices", []) for i in d.get("interfaces", []) }

    # Build device-level graph
    G = nx.Graph()
    for d in devices.values():
        G.add_node(d["id"], label=d.get("label", d["id"]))

    # Add edges and collect diagnostics
    unknown_devices = set()
    unknown_ifaces = set()
    duplicate_links = []
    seen = set()

    for link in topo.get("links", []):
        a_dev = link.get("a", {}).get("device")
        b_dev = link.get("b", {}).get("device")
        a_if  = link.get("a", {}).get("iface")
        b_if  = link.get("b", {}).get("iface")

        # Device checks
        if a_dev not in devices: unknown_devices.add(a_dev)
        if b_dev not in devices: unknown_devices.add(b_dev)

        # Interface checks
        if (a_dev, a_if) not in iface_ids: unknown_ifaces.add((a_dev, a_if))
        if (b_dev, b_if) not in iface_ids: unknown_ifaces.add((b_dev, b_if))

        # Add edge (device-level)
        if a_dev and b_dev:
            key = tuple(sorted([a_dev, b_dev]) + [a_if or "", b_if or ""])
            if key in seen:
                duplicate_links.append((a_dev, b_dev, a_if, b_if))
            seen.add(key)
            G.add_edge(a_dev, b_dev, label=edge_label(link))

    # ----- Plot -----
    pos = nx.spring_layout(G, seed=7)  # deterministic-ish layout
    nx.draw(G, pos, with_labels=True)  # default styling
    edge_labels = nx.get_edge_attributes(G, "label")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

    plt.title("Topology Verification (device-level, edge labels show interfaces)")
    plt.tight_layout()
    plt.show()

    # ----- Diagnostics -----
    print("\n=== Topology Checks ===")
    print(f"Devices: {len(G.nodes)} | Links: {len(G.edges)}")
    if unknown_devices:
        print("Unknown devices referenced by links:", sorted(d for d in unknown_devices if d))
    if unknown_ifaces:
        print("Unknown interfaces referenced by links:", sorted([f"{d}:{i}" for d,i in unknown_ifaces if d and i]))
    if duplicate_links:
        print("Duplicate links (same device pair & interfaces):")
        for d1, d2, i1, i2 in duplicate_links:
            print(f"  {d1}:{i1} <-> {d2}:{i2}")
    if not any([unknown_devices, unknown_ifaces, duplicate_links]):
        print("No issues found ")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python verify_topology.py <topology.json>")
        sys.exit(1)
    main(sys.argv[1])
