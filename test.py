#!/usr/bin/env python3
import json, sys, difflib

# Define optional fields by category
OPTIONAL_LIST_FIELDS = {"tags"}
OPTIONAL_STRING_FIELDS = {"description", "templateName", "osType", "name", "type"}
OPTIONAL_INTERFACE_FIELDS = {"ipv4Addr", "macAddr"}
OPTIONAL_NETWORK_FIELDS = {"maximumBandwidth"}
OPTIONAL_DEFAULT_FIELDS = {"bandwidth", "latency", "jitter", "loss", "corruption", "mtu"}

def normalize(obj):
    """Normalize JSON recursively for fair comparison (fill in optional fields)."""
    if isinstance(obj, dict):
        norm = {}

        # --- Ensure optional fields exist with defaults ---
        if "tags" not in obj:
            obj["tags"] = []

        for f in OPTIONAL_STRING_FIELDS:
            if f not in obj:
                obj[f] = ""

        for f in OPTIONAL_INTERFACE_FIELDS:
            if f not in obj:
                obj[f] = ""

        for f in OPTIONAL_NETWORK_FIELDS:
            if f not in obj:
                obj[f] = ""

        if "defaults" in obj:
            defaults = obj.get("defaults") or {}
            for f in OPTIONAL_DEFAULT_FIELDS:
                if f not in defaults:
                    defaults[f] = ""
            obj["defaults"] = defaults

        # --- Normalize values ---
        for k, v in obj.items():
            if k in OPTIONAL_LIST_FIELDS:
                if not v:
                    norm[k] = []
                elif isinstance(v, str):
                    norm[k] = [t for t in v.split(";") if t]
                else:
                    norm[k] = v
            elif k in OPTIONAL_STRING_FIELDS or k in OPTIONAL_INTERFACE_FIELDS or k in OPTIONAL_NETWORK_FIELDS:
                norm[k] = v if v else ""
            elif k == "defaults":
                # Normalize defaults dict recursively
                norm[k] = {dk: (dv if dv else "") for dk, dv in v.items()}
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
        print("❌ Topologies differ (after normalization):\n")
        # Pretty print both JSONs with sorted keys for stable diff
        text1 = json.dumps(topo1, indent=2, sort_keys=True).splitlines()
        text2 = json.dumps(topo2, indent=2, sort_keys=True).splitlines()
        diff = difflib.unified_diff(
            text1, text2,
            fromfile=file1, tofile=file2,
            lineterm=""
        )
        for line in diff:
            print(line)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: compare_topologies.py <topology1.json> <topology2.json>")
        sys.exit(2)
    main(sys.argv[1], sys.argv[2])
