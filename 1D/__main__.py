# NOTE: EBotTracker orientation isn't working correctly yet
from time           import sleep

from cv             import get_points
from EBot           import EBot
from still          import download_still
from utils          import Point

import fb

import traceback

# general config
SLEEP_TIME = 0.4

# image stuff
IMG_SAVE_NAME = 'temp.bmp'
IMG_URL = 'http://10.21.141.141/html/cam_pic.php'

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

        print points

        if not i % 10:
            fb.update(points)

        ebot.front = Point(*points['blue'])
        ebot.back  = Point(*points['green'])
        target     = Point(*points['red'])

        if not ebot.front.exists or not ebot.back.exists:
            print 'whoops, green or blue not found. Skip!!'
            continue

        if target.exists:
            # ALIGNMENT
            if not ebot.is_aligned_to(target):
                ebot.stop()
                ebot.align_to(target)
                print 'aligned!\n\n'
            # MOVEMENT
            ebot.move(speed=1, time=0.1)
            print 'eBot marching!'
        else:
            ebot.stop()
            print 'EBOT ON TARGET!'

        sleep(SLEEP_TIME)

        # GENERAL ERROR HANDLING
    except KeyboardInterrupt:
        break
    except ZeroDivisionError:
        print 'Whoops! Divided by 0! Let\'s keep going!'
        traceback.print_exc()
    except Exception, e:
        print 'PROBREM: {}'.format(e)
        traceback.print_exc()
        break

ebot.disconnect()
