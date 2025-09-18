#!/usr/bin/env python3
import json
import sys

def normalize(obj):
    """Normalize JSON recursively for fair comparison."""
    if isinstance(obj, dict):
        norm = {}
        for k, v in obj.items():
            if k == "tags":
                # tags should always be a list
                if not v: 
                    norm[k] = []
                elif isinstance(v, str):
                    norm[k] = [t for t in v.split(";") if t]
                else:
                    norm[k] = v
            else:
                norm[k] = normalize(v)
        return norm
    elif isinstance(obj, list):
        return [normalize(x) for x in obj]
    else:
        return obj if obj is not None else ""

def main(file1, file2):
    with open(file1) as f1, open(file2) as f2:
        topo1 = normalize(json.load(f1))
        topo2 = normalize(json.load(f2))

    if topo1 == topo2:
        print("✅ Topologies are semantically equivalent.")
        sys.exit(0)
    else:
        print("❌ Topologies differ (after normalization).")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: compare_topologies.py <topology1.json> <topology2.json>")
        sys.exit(2)
    main(sys.argv[1], sys.argv[2])
