from time      import sleep

from constants import CAMERA_X_MAX, CAMERA_Y_MAX, GRID_X_MAX, GRID_Y_MAX, FAN_BASE_URL
from fb        import fb
from helpers   import log, tlog, unblock

import requests

UPDATE_INTERVAL = 1

class State(object):
    def __init__(self):
        self.heatmap = fb.get('/grid') or [range(max_x+1) for y in range(max_y+1)]
        self.is_on = False
        self.r     = None
        self.prev_target = None
        self.regions = {}

        unblock(self.update_state)

    def update_state(self):
        while True:
            log('Updating State....', color='gray')
            db = fb.get('/')

            was_on     = self.is_on
            self.is_on = db['Power']
            if self.is_on != was_on:
                pass
                # log('changing', color='red')
                # self.set_fan_power()

            for y in range(3):
                for x in range(3):
                    self.regions[(x, y)] = db['onRegions({}, {})'.format(x,y)]

            # log(self.is_on, color='gray')
            # log(self.regions, color='gray')
            log('State updated!', color='gray')

            sleep(UPDATE_INTERVAL)

    def set_fan_power(self):
        if self.r:
            self.r.close()
        if self.is_on:
            self.r = requests.get('{}on'.format(FAN_BASE_URL))
        else:
            self.r = requests.get('{}off'.format(FAN_BASE_URL))

        # log('fan updated', color='green')

    def point_to_region(self, point):
        x = int(point.x / CAMERA_X_MAX * 3)
        y = int(point.y / CAMERA_Y_MAX * 3)

        return x, y

    def is_in_on_region(self, point):
        x, y = self.point_to_region(point)

        return self.regions.get((x,y), 0)

    def track_target(self, point):
        if not point.exists and self.prev_target:
            point = self.prev_target

        self.prev_target = point
        x = int(point.x / CAMERA_X_MAX * GRID_X_MAX)
        y = int(point.y / CAMERA_Y_MAX * GRID_Y_MAX)

        self.heatmap[y][x] += 1

        print 'tracking ({}, {})'.format(x,y)
        fb.put('/grid/{}/'.format(y), str(x), self.heatmap[y][x])

state = State()
