import time
import pycore
import random

def i(cc_core, s):
    cc_core.log_info(s)

def e(cc_core, s):
    cc_core.log_error(s)

TIMEOUT_MS = 2000
NAMESPACE = "enemy_zone"
ASSET_ID = "ENEMY123"

# Function to build createAsset mutation
def create_asset_data(x, y):
    return f"""
    mutation newAsset {{
        createAsset(input: {{
            assetData: {{
                type: "ENEMY",
                name: "EnemyAsset",
                packageName: "ENEMY_PACKAGE",
                sId: "{ASSET_ID}",
                location: {{
                    latitude: {x},
                    longitude: {y},
                    altitude: 10.0
                }},
                initialFuel: 100.0
            }}
        }}) {{
            asset {{
                id
                name
            }}
        }}
    }}
    """

# Function to build updateAsset mutation
def update_asset_data(x, y):
    return f"""
    mutation updateAsset {{
        updateAsset(input: {{
            sId: "{ASSET_ID}",
            location: {{
                latitude: {x},
                longitude: {y},
                altitude: 10.0
            }}
        }}) {{
            asset {{
                id
                name
            }}
        }}
    }}
    """

def run_service(move_count=10):
    print("START <Enemy Asset Movement Service>")
    cc_core = None
    try:
        cc_core = pycore.setup()
        i(cc_core, f"Using pycore lib [{pycore.lib_core_version()}]")

        part_meta = pycore.IsdParticipantMetadata(
            cc_core,
            "EnemyService",
            {NAMESPACE: ["asset() -> list[assets]", "asset(name) -> Asset"]},
            {NAMESPACE: ["createAsset() -> Asset", "updateAsset() -> Asset"]},
            {NAMESPACE: ["assetCreated() -> Asset"]},
            {}
        )

        req_id = cc_core.new_uuid()
        participant = cc_core.register(req_id, part_meta, TIMEOUT_MS)
        i(cc_core, f"Participant registered with ID: [{participant.participant_id()}]")

        # Initial position
        x, y = 0.0, 0.0

        # First, create the asset
        print("Creating initial asset...")
        create_req_id = cc_core.new_uuid()
        create_operation = create_asset_data(x, y)
        write_qos = pycore.qos.new()
        write_qos.set_durability_volatile()
        write_qos.set_ownership_shareable_intra_asset()
        result = participant.write(cc_core, create_req_id, NAMESPACE, create_operation, write_qos)
        for r in result.responses():
            print(f"Asset created at ({x:.4f}, {y:.4f}) | Response: {r.result()}")

        # Now loop to update the asset's position
        for _ in range(move_count):
            x += random.uniform(-0.01, 0.01)
            y += random.uniform(-0.01, 0.01)

            update_req_id = cc_core.new_uuid()
            update_operation = update_asset_data(x, y)
            result = participant.write(cc_core, update_req_id, NAMESPACE, update_operation, write_qos)
            for r in result.responses():
                print(f" Updated position to ({x:.4f}, {y:.4f}) | Response: {r.result()}")

            time.sleep(1)

    except KeyboardInterrupt:
        print("Service stopped by user.")
    except Exception as ex:
        print(f"EXCEPTION: {ex}")
    finally:
        if cc_core:
            cc_core.close()

if __name__ == "__main__":
    run_service()
