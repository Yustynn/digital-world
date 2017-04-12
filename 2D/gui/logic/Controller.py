'''
# PD vs P
We use a proportional derivative control. This is to reduce the amplitude of
oscillation between being too far above (too hot) or too far below (too cold)
the target temperature.

The proportional derivative controller, to use a physical analogy, attempts to
get us to the target temperature as fast as possible. In doing so, it induces a
'momentum' which causes us to exceed this target temperature when reached,
which in turn induces a negative error, causing it to 'decelerate' and eventually
swing back the other way around. This cycles, creating a large error oscillation.

Extending this analogy, the derivative controller, being perpertually in the
opposite direction to the proportional controller, acts to 'slow down' the descent
of the temperature, thereby reducing the overshoot.

# Why Those k Values?
From the optimization problem we solved in math, these k values best
minimize the overall error.

# Interesting Observation
A binary controller seems like it would do the same job here.
This is likely due to the resolution of temperature readings
Not being sufficient to have any sort of intermediate power states
between fully on (1) and off (0).

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
    def __init__(self, target_temp=30.0, ks=[5.69, 5.84, 4.9, 3.64]):
        # negate ks because we're trying to DECREASE temperatur
        self.ks = [float(-k) for k in ks]

        self.target_temp = target_temp

        self.prev_time = time()
        self.es = []
        self.startState = None

    def getNextValues(self, state, temp):
        curr_time = time()
        ks, es = self.ks, self.es

        e = self.target_temp - temp
        es.append(e)
        
        # ensure we aren't needlessly tracking values
        if len(es) > len(ks):
            es.pop(0)

        # if we don't have err values for nth terms, use old ones
        for idx, k in enumerate(ks):
            if len(es) <= idx:
                es.insert(0, es[-1])

        power = 0.0
        for i in range( len(ks) ):
            power += ks[i] * es[i]

        # our increments of time may not be constant
        delta_time = curr_time - self.prev_time

        power /= delta_time
        power = norm(power, 1.0)

        if power < 0:
            power = 0

        self.prev_time = curr_time

        return None, Powers(power, power)

if __name__ == '__main__':
    from doctest import testmod
    testmod()
