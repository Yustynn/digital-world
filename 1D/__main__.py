# NOTE: EBotTracker orientation isn't working correctly yet

from firebase       import firebase
from time           import sleep

from cv             import get_points
from EBot           import EBot
from still          import download_still
from utils          import Point

import traceback

# general config
SLEEP_TIME = 0.4

# image stuff
IMG_SAVE_NAME = 'temp.bmp'
IMG_URL = 'http://10.21.141.141/html/cam_pic.php'

# firebase setup
URL = "https://dw-1d-ebot.firebaseio.com/"
TOKEN = "avxnAEHlshI3X9XUYWpa88AgOsbBmx30DdSV6hqN"

fb = firebase.FirebaseApplication(URL, TOKEN)

print 'Initializing eBot...'
ebot = EBot()
print 'eBot initialized!'

i = 0

while True:
    try:
        i += 1
        print '\n\n{:-^80}\n'.format('ITERATION ' + str(i))
        # LOCALIZATION
        download_still(IMG_URL, IMG_SAVE_NAME)
        points = get_points(IMG_SAVE_NAME)

        ebot.front = Point(*points['blue'])
        ebot.back  = Point(*points['green'])
        target     = Point(*points['red'])

        print points

        if ebot.back.x == 256:
            print 'whoops, green error. Next!'
            continue 


        # # FIREBASE UPDATE
        # print 'Updating firebase...'
        # try:
        #     for key, point in points.iteritems():
        #         fb.put('/', key, point)
        #     print 'Firebase updated!'
        # except KeyboardInterrupt:
        #     break
        # except:
        #     print 'Firebase update failed'

        # ALIGNMENT
        if ebot.is_aligned_to(target):
            ebot.stop()
            pass
        else:
            ebot.align_to(target)
            print 'aligned!\n\n'

        sleep(SLEEP_TIME)

        # GENERAL ERROR HANDLING
    except KeyboardInterrupt:
        break
    except ZeroDivisionError:
        print 'Whoops! Divided by 0!'
        traceback.print_exc()
    except Exception, e:
        print 'PROBREM: {}'.format(e)
        traceback.print_exc()
        break

ebot.disconnect()
