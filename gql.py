from pycore import IsdOperationParams

class WriteUpdateAssetPosition:
    def __init__(self, asset_name, latitude, longitude, altitude):
        self.asset_name = asset_name
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude

    def to_gql(self):
        mutation = """
        mutation UpdateAssetPosition(
            $asset_name: String!, 
            $latitude: Float!, 
            $longitude: Float!, 
            $altitude: Float!
        ) {
            updateAssetPosition(
                assetName: $asset_name, 
                latitude: $latitude, 
                longitude: $longitude, 
                altitude: $altitude
            ) {
                success
                message
            }
        }
        """
        params = IsdOperationParams()
        params.add_str("asset_name", self.asset_name)
        params.add_float("latitude", self.latitude)
        params.add_float("longitude", self.longitude)
        params.add_float("altitude", self.altitude)
        
        return mutation, params
