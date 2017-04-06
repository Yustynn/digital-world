# NOTE: EBotTracker orientation isn't working correctly yet

from firebase   import firebase
from time       import sleep

from cv         import get_points
from still      import download_still
from utils       import EBotTracker, Point

# general config
SLEEP_TIME = 0.1

# image stuff
IMG_SAVE_NAME = 'temp.bmp'
IMG_URL = 'http://10.21.113.183/html/cam_pic.php'

# firebase setup
URL = "https://dw-1d-ebot.firebaseio.com/"
TOKEN = "avxnAEHlshI3X9XUYWpa88AgOsbBmx30DdSV6hqN"

fb = firebase.FirebaseApplication(URL, TOKEN)
e = EBotTracker()

while True:
    download_still(IMG_URL, IMG_SAVE_NAME)
    points = get_points(IMG_SAVE_NAME)
    e.front = Point(points['green'])
    e.back  = Point(points['blue'])

    print points
    print e.orientation

    for key, point in points.iteritems():
        fb.put('/', key, point)

    sleep(SLEEP_TIME)
