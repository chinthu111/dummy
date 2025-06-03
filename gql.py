from common import ct

def WriteUpdateAssetPosition(asset_name, latitude, longitude, altitude):
    return {
        "op": "UpdateAssetPosition",
        "params": {
            "asset_name": asset_name,
            "latitude": latitude,
            "longitude": longitude,
            "altitude": altitude
        }
    }
