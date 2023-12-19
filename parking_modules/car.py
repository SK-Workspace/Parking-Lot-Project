class Car:
    def __init__(self, license_plate):
        self.license_plate = license_plate

    def __str__(self):
        return f"Car with license plate {self.license_plate}"

    def park(self, parking_lot, spot_number):
        if parking_lot.parking_spots[spot_number-1] is None:
            parking_lot.parking_spots[spot_number-1] = self
            return f"Car with license plate {self.license_plate} parked successfully in spot {spot_number}"
        else:
            return f"Spot {spot_number} is occupied, please choose another spot to park"