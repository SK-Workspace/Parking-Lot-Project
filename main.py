import random
import string
from parkinglot import ParkingLot
from car import Car

# Generate N sized array with random car lincese plates
def randomCarLicenseGen(N=0):
    return [''.join(random.choices(string.ascii_uppercase+string.digits,k=7)) for i in range(N)]

def main(carsLicensePlates=[]):
    # Create a parking lot of 2000 square feet
    parking_lot = ParkingLot(2000)
    
    # Create an array of cars with random license plates
    cars = [Car(carsLicensePlates[i]) for i in range(len(carsLicensePlates))]

    # Park the cars in the parking lot
    while cars and parking_lot.available_spots() > 0:
        spot_number = random.randint(1, parking_lot.total_spots)
        status = cars[0].park(parking_lot, spot_number)
        if cars[0] in parking_lot.parking_spots:
           cars.pop(0)
        print(status)
    else:
        print('\n<<===Start of Summary===>>')
        print('\n{} car(s) need to be parked in {} spot(s) of total size {}ft\u00b2 with each spot of size {}ft\u00b2'\
            .format(len(carsLicensePlates),parking_lot.total_spots,parking_lot.total_size, parking_lot.spot_width * parking_lot.spot_length ))
        print('\n{} car(s) successfully parked: \n{}'\
               .format(len([i for i in parking_lot.parking_spots if i]),\
                    {spot.license_plate:i+1 for i,spot in enumerate(parking_lot.parking_spots) if spot}))
        print('\n{} cars waiting for parking: \n{}'\
               .format(len(cars),[i.license_plate for i in cars]))
        print('\n<<===End of Summary===>>')

    # Upload file to S3
    parking_lot.uploadS3Object()



if __name__ == "__main__":
    #Generate N random car license plates using randomCarLicenseGen(N) and pass it to main method/function
    main(randomCarLicenseGen(42))