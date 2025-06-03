from pycore import IsdOperationParams

class WriteUpdateAssetPosition:
    def __init__(self, asset_name, latitude, longitude, altitude):
        self.asset_name = asset_name
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude

    def to_gql(self):
        # Construct the GraphQL mutation
        mutation = """
        mutation UpdateAssetPosition($asset_name: String!, $lat: Float!, $lon: Float!, $alt: Float!) {
            updateAssetPosition(assetName: $asset_name, latitude: $lat, longitude: $lon, altitude: $alt) {
                success
                message
            }
        }
        """
        # Create a dict of parameters
        params_dict = {
            "asset_name": self.asset_name,
            "lat": self.latitude,
            "lon": self.longitude,
            "alt": self.altitude
        }
        # Convert dict to IsdOperationParams
        op_params = IsdOperationParams(params_dict)
        return mutation, op_params
