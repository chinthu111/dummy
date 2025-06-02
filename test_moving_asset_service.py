import moving_asset_service

def test_moving_asset():
    print("Running Moving Asset Test")
    # Run the service with a limited number of moves (e.g., 5 for quick test)
    moving_asset_service.run_service(move_count=5)
    print("Test completed successfully")

if __name__ == "__main__":
    test_moving_asset()
