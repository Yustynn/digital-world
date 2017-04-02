from libdw.sm import SM
from collections import namedtuple
from TempReader import TempReader

class Controller(SM):
    Powers = namedtulpe('Powers', ['water_pump', 'fan'])

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


