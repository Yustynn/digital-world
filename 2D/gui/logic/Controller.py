from libdw.sm import SM
from collections import namedtuple
from TempReader import TempReader

Powers = namedtuple('Powers', ['water_pump', 'fan'])

class Controller(SM):
    '''
    >>> c = Controller(25)
    >>> c.start()

    Below target

    >>> c.step(23)
    Powers(water_pump=0.0, fan=0.0)

    At target

    >>> c.step(25)
    Powers(water_pump=0.0, fan=0.0)

    Above target

    >>> c.step(26)
    Powers(water_pump=1.0, fan=1.0)
    '''

    def __init__(self, target_temp):
        self.target_temp = target_temp
        self.startState = None

    def getNextValues(self, state, temp):
        if temp > self.target_temp:
            powers = Powers(1.0, 1.0)
        else:
            powers = Powers(0.0, 0.0)

        # this should be a functional state machine (lol) but the requirements
        # stated that there must be some state transitions. So here, have your
        # needless state.
        return powers, powers

controller = Controller(state.target_temp)

if __name__ == '__main__':
    from doctest import testmod
    testmod()
