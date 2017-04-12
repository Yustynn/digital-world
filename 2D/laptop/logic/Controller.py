'''
We use a proportional derivative control. This is to reduce the amplitude of
oscillation between being too far above (too hot) or too far below (too cold)
the target temperature.

The proportional derivative controller, to use a physical analogy, attempts to
get us to the target temperature as fast as possible. In doing so, it induces a
'momentum' which causes us to exceed this target temperature when reached,
which in turn induces a negative error, causing it to 'decelerate' and eventually
swing back the other way around. This cycles, creating a large error oscillation.

Extending this analogy, the derivative controller, being perpertually in the
opposite direction to the proportional controller, acts to 'slow down' the

'''

from libdw.sm    import SM
from collections import namedtuple
from time        import time

Powers = namedtuple('Powers', ['pump', 'fan'])

def norm(v, lim):
    if v >= 0:
        return min(v, lim)
    return max(v, -lim)

class Controller(SM):
    def __init__(self, target_temp=30.0, kp=-1.0991, kd=-0.5286):
        self.kp = float(kp)
        self.kd = float(kd)
        self.target_temp = target_temp

        self.prev_time = time()

        self.startState = None

    def getNextValues(self, state, temp):
        curr_time = time()
        err = self.target_temp - temp

        if hasattr(self, 'prev_err'):
            prev_err = self.prev_err
        else:
            prev_err = err

        kp, kd, prev_time = self.kp, self.kd, self.prev_time

        d_e = (err - prev_err)/(curr_time - prev_time)

        power = kp*err + kd*d_e
        power = norm(power, 1.0)

        if power < 0:
            power = 0

        self.prev_err  = err
        self.prev_time = curr_time

        return None, Powers(power, power)

if __name__ == '__main__':
    from doctest import testmod
    testmod()
