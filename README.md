
<h1>Parking Lot Project:</h1>
<p>
Create a parking lot class that takes in a square footage size as input and creates an array of empty values based on the input square footage size. Assume every parking spot is 8x12 (96 ft2) for this program, but have the algorithm that calculates the array size be able to account for different parking spot sizes. For example, a parking lot of size 2000ft2 can fit 20 cars, but if the parking spots were 10x12 (120 ft2), it could only fit 16 cars. The size of the array will determine how many cars can fit in the parking lot.

Create a car class that takes in a 7 digit license plate and sets it as a property. The car will have 2 methods:
<ol>
<li>
A magic method to output the license plate when converting the class instance to a string.
</li>
<li>
A "park" method that will take a parking lot and spot # as input and fill in the selected spot in the parking lot. If another car is parked in that spot, return a status indicating the car was not parked successfully. If no car is parked in that spot, return a status indicating the car was successfully parked.
</li>
<li>
Create a method for the parking lot class that maps vehicles to parked spots in a JSON object. Call this method at the end of the program, save the object to a file, and upload the file to an input S3 bucket
</li>
</ol>
Have a main method take an array of cars with random license plates and have them park in a random spot in the parking lot array until the input array is empty or the parking lot is full. If a car tries to park in an occupied spot, have it try to park in a different spot instead until it successfully parks. Once the parking lot is full, exit the program.
Output when a car does or does not park successfully to the terminal (Ex. "Car with license plate [LICENSE_PLATE] parked successfully in spot [SPOT #]").
</p>

<h1>Solution:</h1>
<h2>Importing Necessary Modules</h2>
<pre><code>
import random
import string
import traceback
from collections import deque
from parking_modules.parkinglot import ParkingLot
from parking_modules.car import Car
import parking_modules.config_s3 as cfg
</code></pre>
<p>This section imports all the necessary modules and classes. <code>random</code> and <code>string</code> are standard Python libraries used for generating random strings. <code>traceback</code> is used for printing stack traces. <code>deque</code> is a class from the <code>collections</code> module that allows efficient appending and popping from both ends of a list. <code>ParkingLot</code> and <code>Car</code> are classes from a custom package called <code>parking_modules</code>. <code>config_s3</code> is a module in the same package for configuring S3 uploads.</p>

<h2>Function: randomCarLicenseGen</h2>
<pre><code>
def randomCarLicenseGen(N=0):
    """
    Generates an array of N random car license plates.
    Each license plate is a string of 7 characters containing uppercase letters and digits.
    """
    return [''.join(random.choices(string.ascii_uppercase+string.digits,k=7)) for i in range(N)]
</code></pre>
<p>This function generates an array of <code>N</code> random car license plates. Each license plate is a string of 7 characters containing uppercase letters and digits.</p>

<h2>Main Function</h2>
<pre><code>
def main(carsLicensePlates=[]):
    """
    Main function to park the cars in the parking lot and upload the parking lot status to S3.
    
    Parameters:
    carsLicensePlates (list): List of car license plates.
    """
</code></pre>
<p>This is the main function. It takes a list of car license plates as input.</p>

<h3>Creating a Parking Lot</h3>
<pre><code>
    # Create a parking lot of 2000 square feet
    parking_lot = ParkingLot(2000)
</code></pre>
<p>Here, a new instance of the <code>ParkingLot</code> class is created with a size of 2000 square feet.</p>

<h3>Creating Cars</h3>
<pre><code>
    # Create an array of cars with random license plates
    cars = deque([Car(carsLicensePlates[i]) for i in range(len(carsLicensePlates))])
</code></pre>
<p>This line creates a deque (double-ended queue) of <code>Car</code> objects. Each <code>Car</code> object is initialized with a license plate from the <code>carsLicensePlates</code> list.</p>

<h3>Parking the Cars</h3>
<pre><code>
    # Park the cars in the parking lot
    while cars and parking_lot.available_spots() > 0:
        spot_number = random.randint(1, parking_lot.total_spots)
        status = cars[0].park(parking_lot, spot_number)
        if cars[0] == parking_lot.parking_spots[spot_number-1]:
           cars.popleft()
        print(status)
</code></pre>
<p>This block of code attempts to park each car in the <code>cars</code> deque in the parking lot. It randomly selects a spot number and tries to park the car in that spot. If the car is successfully parked (i.e., the car object is the same as the one in the selected parking spot), it removes the car from the deque. It prints the status of each parking attempt.</p>

<h3>Printing the Summary</h3>
<pre><code>
    else:
        print('\n<<===Start of Summary===>>')
        print(f'\n{len(carsLicensePlates)} car(s) need to be parked in {parking_lot.total_spots} spot(s) of total size {parking_lot.total_size}ft\u00b2 with each spot of size {parking_lot.spot_width * parking_lot.spot_length}ft\u00b2')
        print(f'\n{parking_lot.total_spots-int(parking_lot.available_spots())} car(s) successfully parked')
        print(f'\n{len(cars)} car(s) waiting for parking')
        print('\n<<===End of Summary===>>\n')
</code></pre>
<p>This block of code prints a summary of the parking situation once all cars have been attempted to be parked. It prints the total number of cars, the total number of spots in the parking lot, the total size of the parking lot, the size of each spot, the number of cars successfully parked, and the number of cars still waiting to be parked.</p>

<h3>Configuring S3 Upload</h3>
<pre><code>
    # Make relevant changes in *.ini and create a configuration for s3 upload
    kwargs=cfg.config(configFilename="config_credentials.ini", configSection="aws_s3_credentials")
</code></pre>
<p>This line reads the AWS S3 credentials from a configuration file and stores them in a dictionary. The dictionary is then passed as keyword arguments to the <code>uploadS3Object</code> method.</p>

<h3>Uploading to S3</h3>
<pre><code>
    # Upload file to S3 using configurations
    if kwargs is not None: 
        parking_lot.uploadS3Object(**kwargs)
    else:
        print("Params object is empty. Ensure the object is not empty when calling uploadS3Object()")
        traceback.print_stack()
</code></pre>
<p>This block of code attempts to upload the parking lot status to S3. If the credentials dictionary is not empty, it calls the <code>uploadS3Object</code> method of the <code>ParkingLot</code> class with the credentials as arguments. If the dictionary is empty, it prints an error message and a stack trace.</p>

<h2>Script Entry Point</h2>
<pre><code>
if __name__ == "__main__":
    """
    Entry point of the script.
    Generates N random car license plates using randomCarLicenseGen(N) and passes it to the main function.
    """
    main(randomCarLicenseGen(42))
</code></pre>
<p>This is the entry point of the script. If the script is run directly (as opposed to being imported as a module), it generates 42 random car license plates using the <code>randomCarLicenseGen</code> function and passes them to the <code>main</code> function.</p>

<p>This script creates a parking lot and parks cars with randomly generated license plates in the parking lot. It then uploads the parking lot status to S3. The number of cars and their license plates are generated by the <code>randomCarLicenseGen</code> function. The <code>main</code> function handles the creation of the parking lot, parking of the cars, and uploading the parking lot status to S3. The script starts executing from the <code>if __name__ == "__main__":</code> block.</p>

<p>This detailed explanation should help viewers understand the code better. If there are any more questions or need for further clarification, feel free to ask. Happy coding! 🚀</p>
