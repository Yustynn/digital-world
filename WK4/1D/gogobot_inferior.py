import RPi.GPIO as GPIO
from time import sleep
from firebase import firebase

BUTTON_SLEEP = 0.5

url = "https://my-awesome-project-65917.firebaseio.com/" # URL to Firebase database
token = "h2w4wXwW5dUhSB6jbAxa55JrU1qcEpHxxdK4FolM" # unique token used for authentication

# Create a firebase object by specifying the URL of the database and its secret token.
# The firebase object has functions put and get, that allows user to put data onto
# the database and also retrieve data from the database.
firebase = firebase.FirebaseApplication(url, token)

# Use the BCM GPIO numbers as the numbering scheme
GPIO.setmode(GPIO.BCM)

# Use GPIO12, 16, 20 and 21 for the buttons.
buttons = {'ok': 25, 'left': 18, 'up': 23, 'right': 24}

# Set GPIO numbers in the list: [12, 16, 20, 21] as input with pull-down resistor.
GPIO.setup(buttons.values(), GPIO.IN, GPIO.PUD_DOWN)

# Keep a list of the expected movements that the eBot should perform sequentially.
movement_list = []

done = False

while not done:
    for key, val in buttons.iteritems():
        if key == 'ok':
            firebase.put('/','movement_list', movement_list)
            done = True
        elif GPIO.input(val):
            movement_list.append(key)
            sleep(BUTTON_SLEEP)



# Write to database once the OK button is pressed
