import random
import string
import traceback
from collections import deque
from parking_modules.parkinglot import ParkingLot
from parking_modules.car import Car
import parking_modules.config_s3 as cfg

# Generate N sized array with random car lincese plates
def randomCarLicenseGen(N=0):
    return [''.join(random.choices(string.ascii_uppercase+string.digits,k=7)) for i in range(N)]

def main(carsLicensePlates=[]):
    # Create a parking lot of 2000 square feet
    parking_lot = ParkingLot(2000)
    
    # Create an array of cars with random license plates
    cars = deque([Car(carsLicensePlates[i]) for i in range(len(carsLicensePlates))])
    
    # Park the cars in the parking lot
    while cars and parking_lot.available_spots() > 0:
        spot_number = random.randint(1, parking_lot.total_spots)
        status = cars[0].park(parking_lot, spot_number)
        if cars[0] == parking_lot.parking_spots[spot_number-1]:
           cars.popleft()
        print(status)
    else:
        print('\n<<===Start of Summary===>>')
        print(f'\n{len(carsLicensePlates)} car(s) need to be parked in {parking_lot.total_spots} spot(s) of total size {parking_lot.total_size}ft\u00b2 with each spot of size {parking_lot.spot_width * parking_lot.spot_length}ft\u00b2')
        print(f'\n{parking_lot.total_spots-int(parking_lot.available_spots())} car(s) successfully parked')
        print(f'\n{len(cars)} car(s) waiting for parking')
        print('\n<<===End of Summary===>>\n')


    # Make relevant changes in *.ini and create a configuration for s3 upload
    kwargs=cfg.config(configFilename="config_credentials.ini", configSection="aws_s3_credentials")

    # Upload file to S3 using confirgurations
    if kwargs is not None: 
        parking_lot.uploadS3Object(**kwargs)
    else:
        print("Params object is empty. Ensure the object is not empty when calling uploadS3Object()")
        traceback.print_stack()



if __name__ == "__main__":
    #Generate N random car license plates using randomCarLicenseGen(N) and pass it to main method/function
    main(randomCarLicenseGen(42))
    