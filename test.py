---
- name: Validate CSVs and generate topology JSON
  hosts: localhost
  gather_facts: no

  tasks:
    - name: Build topology
      topology_builder:
        nodes: nodes.csv
        interfaces: interfaces.csv
        networks: networks.csv
        out: topology.json
        scripts_dir: scripts   # helper scripts live here
