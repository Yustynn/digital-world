from eBot import eBot
from time import sleep
from firebase import firebase

url = "https://my-awesome-project-65917.firebaseio.com/" # URL to Firebase database
token = "h2w4wXwW5dUhSB6jbAxa55JrU1qcEpHxxdK4FolM" # unique token used for authentication

# Create a firebase object by specifying the URL of the database and its secret token.
# The firebase object has functions put and get, that allows user to put data onto
# the database and also retrieve data from the database.
firebase = firebase.FirebaseApplication(url, token)

ebot = eBot.eBot() # create an eBot object
ebot.connect() # connect to the eBot via Bluetooth

# Use a variable to determine whether there is any valid movement commands in
# the Firebase database.
no_commands = True

def move(direction):
    direction_map = {
        'left': (-1,1),
        'right': (1,-1),
        'forward': (1,1)
    }

    ebot.wheels(*direction_map[direction])
    sleep(1)
    ebot.wheels(0,0)

move('left')

directions = firebase.get('/movement_list')

for direction in directions:
    move(direction)

while no_commands:
    # Check the value of movement_list in the database at an interval of 0.5
    # seconds. Continue checking as long as the movement_list is not in the
    # database (ie. it is None). If movement_list is a valid list, the program
    # exits the while loop and controls the eBot to perform the movements
    # specified in the movement_list in sequential order. Each movement in the
    # list lasts exactly 1 second.

    # Get movement list from Firebase
    movement_list = None

    # Write your code here


    sleep(0.5)

# Write the code to control the eBot here


ebot.disconnect() # disconnect the Bluetooth communication
