import time
import pycore
import random

def i(cc_core, s):
    cc_core.log_info(s)

def e(cc_core, s):
    cc_core.log_error(s)

TIMEOUT_MS = 2000
NAMESPACE = "enemy_zone"

def create_asset_data(x, y):
    return f"""
    mutation newAsset {{
        createAsset(input: {{
            assetData: {{
                type: "ENEMY",
                name: "EnemyAsset",
                packageName: "ENEMY_PACKAGE",
                sId: "ENEMY123",
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

def run_service(move_count=10):
    print("START <Enemy Asset Movement Service>")
    cc_core = None
    try:
        cc_core = pycore.setup()
        i(cc_core, f"Using pycore lib [{pycore.lib_core_version()}]")

        part_meta = pycore.IsdParticipantMetadata({
            "TestParticipant": {
                "NAMESPACE": NAMESPACE,
                "Permissions": ["createAsset", "updateAsset"]
            }
        })
        req_id = cc_core.new_uuid()
        participant = cc_core.register(req_id, part_meta, TIMEOUT_MS)
        i(cc_core, f"Participant registered with ID: [{participant.participant_id()}]")

        x, y = 0.0, 0.0

        for _ in range(move_count):
            write_req_id = cc_core.new_uuid()
            write_operation = create_asset_data(x, y)

            write_qos = pycore.qos.new()
            write_qos.set_durability_volatile()
            write_qos.set_ownership_shareable_intra_asset()

            result = participant.write(
                cc_core,
                write_req_id,
                NAMESPACE,
                write_operation,
                write_qos
            )

            for r in result.responses():
                print(f" Moved to ({x:.2f}, {y:.2f}) | Response: {r.result()}")

            x += random.uniform(-0.01, 0.01)
            y += random.uniform(-0.01, 0.01)
            time.sleep(1)

    except KeyboardInterrupt:
        print("Service stopped.")
    except Exception as ex:
        print(f"EXCEPTION: {ex}")
    finally:
        if cc_core:
            cc_core.close()

if __name__ == "__main__":
    run_service()
