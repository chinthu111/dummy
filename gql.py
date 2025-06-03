from pycore import IsdOperationParams

class WriteUpdateAssetPosition:
    def __init__(self, asset_name, latitude, longitude, altitude):
        self.asset_name = asset_name
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude

    def to_gql(self):
        # This is the mutation string; you can adjust the formatting if needed
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
        
        # Create IsdOperationParams with the required parameters
        params = IsdOperationParams()
        params["asset_name"] = self.asset_name
        params["latitude"] = self.latitude
        params["longitude"] = self.longitude
        params["altitude"] = self.altitude
        
        return mutation, params
