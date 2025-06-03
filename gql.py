from pycore import IsdOperationParams

class WriteUpdateAssetPosition:
    def __init__(self, asset_name, latitude, longitude, altitude):
        self.asset_name = asset_name
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude

    def to_gql(self):
        mutation = """
        mutation UpdateAssetPosition($asset_name: String!, $lat: Float!, $lon: Float!, $alt: Float!) {
            updateAssetPosition(assetName: $asset_name, latitude: $lat, longitude: $lon, altitude: $alt) {
                success
                message
            }
        }
        """
        # Proper creation of IsdOperationParams
        op_params = IsdOperationParams()
        op_params.add_param("asset_name", self.asset_name)
        op_params.add_param("lat", self.latitude)
        op_params.add_param("lon", self.longitude)
        op_params.add_param("alt", self.altitude)

        return mutation, op_params
