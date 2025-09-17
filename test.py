#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.basic import AnsibleModule
import subprocess
import os
import sys

DOCUMENTATION = r'''
---
module: topology_builder
short_description: Validate CSV files and generate a topology JSON
description:
  - This module validates infrastructure CSV definitions (nodes, interfaces, networks).
  - If validation passes, it can generate a topology JSON file.
  - Supports validate-only mode for CI/CD pipelines.
version_added: "1.1.0"
author:
  - Your Name (@yourgithub)
options:
  nodes:
    description: Path to the nodes.csv file.
    required: true
    type: str
  interfaces:
    description: Path to the interfaces.csv file.
    required: true
    type: str
  networks:
    description: Path to the networks.csv file.
    required: true
    type: str
  out:
    description: Path for the generated topology JSON file.
    required: false
    type: str
    default: topology.json
  schema:
    description: JSON schema reference.
    required: false
    type: str
    default: https://portal.mipn.co.uk/topologyschema-01/schema#
  python_bin:
    description: Python interpreter to run helper scripts.
    required: false
    type: str
    default: python3
  scripts_dir:
    description: Directory containing validate_topology_csvs.py and generate_topology.py.
    required: false
    type: str
    default: scripts
  validate_only:
    description: If true, only run validation and skip JSON generation.
    required: false
    type: bool
    default: false
notes:
  - Validation runs first. If it fails, generation will not run.
  - Exit codes are mapped for CI/CD usage:
      0 = success
      1 = validation failed
      2 = generation failed
'''

EXAMPLES = r'''
# Validate and generate
- name: Build topology.json
  topology_builder:
    nodes: nodes.csv
    interfaces: interfaces.csv
    networks: networks.csv
    out: topology.json

# Validate only (CI pipeline pre-check)
- name: Validate CSVs only
  topology_builder:
    nodes: nodes.csv
    interfaces: interfaces.csv
    networks: networks.csv
    validate_only: true
'''

RETURN = r'''
msg:
  description: Human-readable result message.
  type: str
  returned: always
stdout:
  description: Raw stdout from underlying scripts.
  type: str
  returned: always
stderr:
  description: Raw stderr from underlying scripts (if any).
  type: str
  returned: on failure
cmd:
  description: The executed command.
  type: str
  returned: always
changed:
  description: Whether topology.json was generated.
  type: bool
  returned: always
'''

def run_command(cmd):
    """Run shell command and capture output"""
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()

def main():
    module = AnsibleModule(
        argument_spec=dict(
            nodes=dict(required=True, type='str'),
            interfaces=dict(required=True, type='str'),
            networks=dict(required=True, type='str'),
            out=dict(default="topology.json", type='str'),
            schema=dict(default="https://portal.mipn.co.uk/topologyschema-01/schema#", type='str'),
            python_bin=dict(default="python3", type='str'),
            scripts_dir=dict(default="scripts", type='str'),
            validate_only=dict(default=False, type='bool'),
        ),
        supports_check_mode=False
    )

    nodes = module.params["nodes"]
    interfaces = module.params["interfaces"]
    networks = module.params["networks"]
    out = module.params["out"]
    schema = module.params["schema"]
    python_bin = module.params["python_bin"]
    scripts_dir = module.params["scripts_dir"]
    validate_only = module.params["validate_only"]

    validate_script = os.path.join(scripts_dir, "validate_topology_csvs.py")
    generate_script = os.path.join(scripts_dir, "generate_topology.py")

    # Step 1: Validation
    validate_cmd = (
        f"{python_bin} {validate_script} "
        f"--nodes {nodes} --interfaces {interfaces} --networks {networks}"
    )
    rc, stdout, stderr = run_command(validate_cmd)
    if rc != 0:
        module.fail_json(
            msg="Validation failed",
            stdout=stdout,
            stderr=stderr,
            cmd=validate_cmd,
            rc=1
        )

    if validate_only:
        module.exit_json(
            changed=False,
            msg="Validation successful (no JSON generated)",
            stdout=stdout,
            cmd=validate_cmd
        )

    # Step 2: Generation
    gen_cmd = (
        f"{python_bin} {generate_script} "
        f"--schema {schema} --nodes {nodes} --interfaces {interfaces} --networks {networks} --out {out}"
    )
    rc, stdout, stderr = run_command(gen_cmd)
    if rc != 0:
        module.fail_json(
            msg="Topology generation failed",
            stdout=stdout,
            stderr=stderr,
            cmd=gen_cmd,
            rc=2
        )

    module.exit_json(
        changed=True,
        msg=f"Topology generated successfully: {out}",
        stdout=stdout,
        cmd=gen_cmd
    )

if __name__ == "__main__":
    main()
