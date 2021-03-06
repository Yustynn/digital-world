from kivy.uix.widget    import Widget
from kivy.properties    import NumericProperty, ObjectProperty

from time               import sleep, time

# self-created mods
import logic.fb as fb
from logic.helpers      import unblock
from constants          import SIM_MODE, UPDATE_INTERVAL

# let's not slow our app down

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
    target_temp      = NumericProperty(fb.get('target_temp'))
    power            = NumericProperty(fb.get('power'))
    temp             = NumericProperty(fb.get('temp'))

    # # For testing, so the app starts off quick without having to wait for HTTP responses
    # target_temp = NumericProperty(0.0)
    # power       = NumericProperty(0.0)
    # temp        = NumericProperty(0.0)

    power_consumed   = NumericProperty(0.0)
    wind_vel         = NumericProperty(0.0)
    sur_temp         = NumericProperty(0.0)
    solar_irradiance = NumericProperty(0.0)

    def __init__(self, sim_mode = SIM_MODE):
        Widget.__init__(self)

        self.power_history = History([(0, self.power)])
        self.temp_history = History([(0, self.temp)])
        self.target_temp_history = History([(0, self.target_temp)])

        self.sim_mode = sim_mode

        if self.sim_mode:
            from sim import bottle, sim_state
            self.bottle    = bottle
            self.sim_state = sim_state

        # non-blocking update logic
        unblock(self.update)

    def update(self):
        while 1:
            if self.sim_mode:
                # grab state
                self.temp     = self.bottle.temp - 273.15
                self.sur_temp = self.sim_state.temp - 273.15
                self.wind_vel = self.sim_state.wind_vel
                self.solar_irradiance = self.sim_state.solar_irradiance
                self.power_consumed   = self.sim_state.power_consumed

                sleep(UPDATE_INTERVAL * 10)

            else:
                # errors sometimes due to HTTP failures
                try:
                    # get latest temp
                    self.temp = fb.get('temp')

                except Exception, e:
                    print 'Failed to retrieve temperature', e

            # track everything
            self.power_history.track(self.power)
            self.target_temp_history.track(self.target_temp)
            self.temp_history.track(self.temp)


    def set(self, key, val):
        # let's avoid drunken behaviour
        if not hasattr(self, key):
            raise NameError('No property called {} in state'.format(key))

        setattr(self, key, val) # optimism

        if not self.sim_mode:
            unblock( lambda: fb.set(key, val) )

state = State()
