from kivy.uix.widget    import Widget
from kivy.properties    import NumericProperty, ObjectProperty

# other mods
from collections        import namedtuple
from functools          import update_wrapper
from threading          import Thread
from time               import time

# self-created mods
import logic.fb as fb

# let's not slow our app down
def unblock(fn):
    t = Thread(target=fn)
    t.daemon = True
    t.start()

# value vs time tracker for getting data points for graph
class History(object):
    def __init__(self, points = [], max_points=10):
        self.max_points = max_points
        self.points = points
        self.start_time = time()

    def track(self, val):
        now = time() - self.start_time
        self.points.append((now, val))

        if len(self.points) > self.max_points:
            self.points.pop(0)

class State(Widget):
    # target_temp = NumericProperty(fb.get('target_temp'))
    # power       = NumericProperty(fb.get('power'))
    # temp        = NumericProperty(fb.get('temp'))

    # # For testing, so the app starts off quick without having to wait for HTTP responses
    target_temp = NumericProperty(0.0)
    power       = NumericProperty(0.0)
    temp        = NumericProperty(0.0)

    def __init__(self):
        Widget.__init__(self)

        self.power_history = History([(0, self.power)])
        self.temp_history = History([(0, self.temp)])

        # non-blocking update logic
        unblock(self.update)

    # errors sometimes due to HTTP failures
    def update(self):
        try:
            # get latest temp
            self.temp = fb.get('temp')

            # track both temp and power
            self.temp_history.track(self.temp)
            self.power_history.track(self.power)

        except Exception, e:
            print 'Failed to retrieve temperature', e

        self.update()

    def set(self, key, val):
        # let's avoid drunken behaviour
        if not hasattr(self, key):
            raise NameError('No property called {} in state'.format(key))

        setattr(self, key, val) # optimism
        unblock( lambda: fb.set(key, val) )

state = State()
