# NOTE: EBotTracker orientation isn't working correctly yet
from time           import sleep

from cv             import get_points
from EBot           import EBot
from helpers        import log, tlog
from State          import state
from still          import download_still
from utils          import Point

import fb

import traceback

# general config
SLEEP_TIME = 0.4

# image stuff
IMG_SAVE_NAME = 'temp.bmp'
IMG_URL = 'http://10.21.141.141/html/cam_pic.php'

log( 'Initializing eBot...' )
ebot = EBot()
log( 'eBot initialized!' )

iteration = 0

while True:
    try:
        iteration += 1
        log( '\n\n{:-^80}\n'.format('ITERATION ' + str(iteration)) )

        # LOCALIZATION
        download_still(IMG_URL, IMG_SAVE_NAME)
        points = get_points(IMG_SAVE_NAME)

        log( points )

        ebot.front = Point(*points['blue'])
        ebot.back  = Point(*points['green'])
        target     = Point(*points['red'])

        if not state.is_in_on_region(target):
            log( 'Target in off region. Pausing for {} seconds'.format(SLEEP_TIME), color='red' )

        if not iteration % 10:
            log( 'Tracking state', color='blue' )
            fb.update_points(points)
            state.track_target(target)

        if not ebot.front.exists or not ebot.back.exists:
            log( 'Front/Back of ebot not found! Moving to next iteration...', color='red' )
            continue

        if target.exists:
            # ALIGNMENT
            if not ebot.is_aligned_to(target):
                ebot.stop()
                ebot.align_to(target)
                log( 'Alignment iteration done!' )
                continue
            # MOVEMENT
            ebot.move(speed=1, time=0.1)
        else:
            ebot.stop()
            log( 'EBOT ON TARGET!', color='green' )

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
