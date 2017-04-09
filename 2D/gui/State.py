from kivy.uix.widget    import Widget
from kivy.properties    import NumericProperty, ObjectProperty

# other mods
from threading          import Thread
from functools          import update_wrapper

# self-created mods
import logic.fb as fb

# let's not slow our app down
def unblock(fn):
    t = Thread(target=fn)
    t.daemon = True
    t.start()

class State(Widget):
    # ideal_temp = NumericProperty(fb.get('ideal_temperature'))
    # power      = NumericProperty(fb.get('power'))
    # temp       = NumericProperty(fb.get('temperature'))

    ideal_temp = NumericProperty(0.0)
    power      = NumericProperty(0.0)
    temp       = NumericProperty(0.0)

    def __init__(self, ideal_temp = 30.0, power = 0.0):
        Widget.__init__(self)

        # non-blocking update logic
        unblock(self.update)

    def update(self):
        self.temp = fb.get('temperature')
        self.update()

    def set(self, key, val):
        if not hasattr(self, key):
            raise NameError('No property called {} in state'.format(key))

        setattr(self, key, val) # let's be optimistic
        unblock( lambda: fb.set(key, val) )

state = State()
