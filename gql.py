def build_update_asset_position(asset_name, latitude, longitude, altitude):
    """
    Constructs the GraphQL mutation to update an asset's position.
    """
    mutation = """
    mutation UpdateAssetPosition($asset_name: String!, $lat: Float!, $lon: Float!, $alt: Float!) {
        updateAssetPosition(assetName: $asset_name, latitude: $lat, longitude: $lon, altitude: $alt) {
            success
            message
        }
    }
    """
    params = {
        "asset_name": asset_name,
        "lat": latitude,
        "lon": longitude,
        "alt": altitude
    }
    return mutation, params
