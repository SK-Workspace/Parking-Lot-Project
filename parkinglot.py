import json
import boto3

class ParkingLot:
    def __init__(self, total_size, spot_width=8, spot_length=12):
        self.spot_width = spot_width
        self.spot_length = spot_length
        self.total_size= total_size
        self.total_spots = total_size // (spot_width * spot_length)
        self.parking_spots = [None] * self.total_spots

    def available_spots(self):
        return self.parking_spots.count(None)

    def uploadS3Object(self):
        # Create an object mapping vehicles to parked spots
        parked_cars = {}
        for i, spot in enumerate(self.parking_spots):
            if spot:
                parked_cars[spot.license_plate] = i + 1
        
        # Convert the object to JSON
        json_data = json.dumps(parked_cars, indent=4)

        # Save the JSON object to a file
        with open('parked_cars.json', 'w') as file:
            file.write(json_data)
        try:
            # Upload the file to S3 bucket and print success message in terminal
            s3 = boto3.client('s3', aws_access_key_id='xxxx',aws_secret_access_key='xxx')
            s3.upload_file('parked_cars.json', 'your-bucket-name', 'parked_cars.json')
            print("\nThe details of the parked car(s) have been successfully \
                uploaded to the Amazon S3 cloud storage. File name: 'parked_cars.json'\n")
        except Exception as err:
            print(f"\n Oops...Somthing went wrong with S3 upload.\n Info: {err}\n ")