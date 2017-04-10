from libdw.sm import SM
from collections import namedtuple

Powers = namedtuple('Powers', ['pump', 'fan'])

def norm(v, lim):
    if v >= 0:
        return min(v, lim)
    return max(v, -lim)

class Controller(SM):
    def __init__(self, target_temp=30.0, k1=-0.3, k2=-0.5):
        self.k1 = float(k1)
        self.k2 = float(k2)
        self.target_temp = target_temp

        self.startState = None

    def getNextValues(self, state, temp):
        err = self.target_temp - temp
        k1, k2   = self.k1, self.k2

        if hasattr(self, 'prev_err'):
            prev_err = self.prev_err
        else:
            prev_err = err

        power = k1*err + k2*prev_err
        power = norm(power, 1.0)

        if power < 0:
            power = 0

        self.prev_err = err

        return None, Powers(power, power)

if __name__ == '__main__':
    from doctest import testmod
    testmod()
