#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import subprocess
import os

def run_command(cmd, cwd=None):
    """Run shell command and capture output"""
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True,
        cwd=cwd
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

    validate_script = os.path.join(scripts_dir, "validate_topology_csvs.py")
    generate_script = os.path.join(scripts_dir, "generate_topology.py")

    # --- Step 1: Validate CSVs ---
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
            cmd=validate_cmd
        )

    # --- Step 2: Generate topology ---
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
            cmd=gen_cmd
        )

    module.exit_json(
        changed=True,
        msg=f"Topology generated successfully: {out}",
        stdout=stdout,
        cmd=gen_cmd
    )

if __name__ == "__main__":
    main()
