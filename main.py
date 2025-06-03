import asyncio
import pycore
import pycorelib
from common.svc_env import ServiceEnv
from common.trajectory import Trajectory
from common.ct import REGISTRATION_TIMEOUT_MS, NAMESPACE_ASSET

# Logging helper functions
def info(cc_core, s):
    cc_core.log_info(s)

def error(cc_core, s):
    cc_core.log_error(s)

async def main():
    svc_env = ServiceEnv.read()
    trajectory_file = svc_env.trajectory_file
    write_period = svc_env.write_period

    trajectory, err_msg = Trajectory.load(trajectory_file)
    if err_msg:
        print(f"Error reading trajectory: {err_msg}")
        return

    cc_core = pycore.setup()

    # Log service details
    info(cc_core, "- Using:")
    info(cc_core, f" corelib [{pycore.lib_core_version()}]")
    info(cc_core, f" pycorelib [{pycorelib.lib_pycore_version()}]")
    info(cc_core, f" Trajectory (csv) file: {svc_env.trajectory_file}")
    info(cc_core, f" Write period (s): {svc_env.write_period}")

    # Setup participant
    participant_name = "dummy_movement_participant"
    read_interests = {}
    write_interests = {}
    listen_interests = {}
    participant_options = {}

    part_meta = pycore.IsdParticipantMetadata(
        cc_core,
        participant_name,
        read_interests,
        write_interests,
        listen_interests,
        participant_options
    )

    req_id = cc_core.new_uuid()

    # Register participant with logging
    try:
        info(cc_core, "- Registering participant")
        info(cc_core, f"Name = [{participant_name}]")
        info(cc_core, f"Request ID [{req_id}]")
        participant = cc_core.register(req_id, part_meta, REGISTRATION_TIMEOUT_MS)
        info(cc_core, "- Participant registered successfully")
    except Exception as e:
        error(cc_core, f"Failed to register participant: {e}")
        return

    # Movement loop
    idx = 0
    total_points = len(trajectory)

    while True:
        point = trajectory[idx]
        idx = (idx + 1) % total_points

        asset_name = "dummy_asset"
        write_op = pycorelib.WriteUpdateAssetPosition(
            asset_name=asset_name,
            latitude=point.latitude,
            longitude=point.longitude,
            altitude=point.altitude,
        )

        operation, params = write_op.to_gql()

        qos = pycore.qos.new()
        qos.set_durability_volatile()
        qos.set_ownership_shareable_intra_inter_asset(0)

        write_req_id = cc_core.new_uuid()
        result = participant.write(cc_core, write_req_id, NAMESPACE_ASSET, operation, qos, params, 2000)
        res = result.responses()[0]

        if res.ok:
            info(cc_core, f"Position updated: {point.latitude}, {point.longitude}, {point.altitude}")
        else:
            error(cc_core, f"Failed to update position: {res.err_msg}")

        await asyncio.sleep(write_period)

if __name__ == "__main__":
    asyncio.run(main())
