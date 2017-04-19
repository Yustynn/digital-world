from time      import sleep

from constants import CAMERA_X_MAX, CAMERA_Y_MAX, GRID_X_MAX, GRID_Y_MAX
from fb        import fb
from helpers   import unblock

UPDATE_INTERVAL = 0.5

class State(object):
    def __init__(self):
        heatmap = fb.get('/grid') or [range(max_x+1) for y in range(max_y+1)]
        self.regions = {}

        unblock(self.update_state)

    def update_state(self):
        while True:
            db = fb.get('/')

            self.is_on = db['Power']

            for y in range(3):
                for x in range(3):
                    self.regions[(x, y)] = db['onRegions({}, {})'.format(x,y)]

            sleep(UPDATE_INTERVAL)

    def is_in_on_region(self, point):
        x = int(point.x / CAMERA_X_MAX)
        y = int(point.y / CAMERA_Y_MAX)

        return getattr(self.regions, (x,y), 0)

    def track_target(self, point):
        x = int(point.x / CAMERA_X_MAX * GRID_X_MAX)
        y = int(point.y / CAMERA_Y_MAX * GRID_Y_MAX)

        self.heatmap[y][x] += 1

        print 'tracking ({}, {})'.format(x,y)
        fb.put('/grid/{}/'.format(y), str(x), heatmap[x][y])

state = State()
