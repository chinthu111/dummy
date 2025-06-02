import asyncio
import pycore
from svc_env import ServiceEnv
from trajectory import Trajectory
from ct import REGISTRATION_TIMEOUT_MS, NAMESPACE_ASSET
import pycorelib

async def main():
    svc_env = ServiceEnv.read()
    trajectory_file = svc_env.trajectory_file
    write_period = svc_env.write_period

    trajectory, err_msg = Trajectory.load(trajectory_file)
    if err_msg:
        print(f"Error reading trajectory: {err_msg}")
        return

    cc_core = pycore.Core()
    cc_core.setup()

    participant_name = "dummy_movement_participant"
    part_meta = pycorelib.IsdParticipantMetadata(
        cc_core, participant_name, read_interests=[], write_interests=[], listen_interests=[]
    )
    req_id = cc_core.new_uuid()
    participant = cc_core.register(req_id, part_meta, REGISTRATION_TIMEOUT_MS)

    print(f"Participant {participant_name} registered")

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
            print(f"Position updated: {point.latitude}, {point.longitude}, {point.altitude}")
        else:
            print(f"Failed to update position: {res.err_msg}")

        await asyncio.sleep(write_period)

if __name__ == "__main__":
    asyncio.run(main())
