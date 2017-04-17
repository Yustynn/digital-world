# NOTE: EBotTracker orientation isn't working correctly yet

from firebase       import firebase
from time           import sleep

from cv             import get_points
from EBot           import EBot
from EBotTracker    import EBotTracker
from still          import download_still
from utils          import Point

import traceback

# general config
SLEEP_TIME = 0.1

# image stuff
IMG_SAVE_NAME = 'temp.bmp'
IMG_URL = 'http://10.21.115.128/html/cam_pic.php'

# firebase setup
URL = "https://dw-1d-ebot.firebaseio.com/"
TOKEN = "avxnAEHlshI3X9XUYWpa88AgOsbBmx30DdSV6hqN"

fb = firebase.FirebaseApplication(URL, TOKEN)

print 'Initializing eBot...'
ebot = EBot()
print 'eBot initialized!'

while True:
    try:
        download_still(IMG_URL, IMG_SAVE_NAME)

        points = get_points(IMG_SAVE_NAME)
        ebot.front = Point(*points['green'])
        ebot.back  = Point(*points['blue'])
        target     = Point(*points['red'])

        print points

        for key, point in points.iteritems():
            fb.put('/', key, point)

        if ebot.is_aligned(target):
            ebot.stop()
        else:
            ebot.align_to(target)
            print 'aligned!\n\n'

        sleep(SLEEP_TIME)
    except KeyboardInterrupt:
        break
    except Exception, e:
        print 'PROBREM: {}'.format(e)
        traceback.print_exc()
        break

# ebot.disconnect()
