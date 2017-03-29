import math
import libdw.util as util
import libdw.sm as sm
import libdw.gfx as gfx
from soar.io import io

# CONSTANTS
DIST      = 0.4
TOLERANCE = 0.05
MOVE_MAG  = 0.2
ROT_MAG   = 0.2

F_SONAR = 2
R_SONAR = 4
L_SONAR = 0

# HELPERS
def in_range(d): return d - DIST < TOLERANCE
def too_close(d): return d < DIST - TOLERANCE

def rotate(dir):
    dirmap = {
        'right': -ROT_MAG,
        'left':   ROT_MAG,
        None:     0
    }

    return io.Action(fvel = 0, rvel = dirmap[dir])

def move(dir):
    dirmap = {
        'forward':  MOVE_MAG,
        'reverse': -MOVE_MAG,
        None:     0
    }

    return io.Action(dirmap[dir], rvel=0)

class MySMClass(sm.SM):
    startState = {
        'move_dir': 'forward',
        'rot_dir': None
    }

    def getNextValues(self, state, inp):
        print inp.odometry.theta
        def outp():
            rot_dir, move_dir = state['rot_dir'], state['move_dir']

            if rot_dir:
                return state, rotate(rot_dir)
            if move_dir:
                return state, move(move_dir)
            return state, move(dir)

        def set_state(rot_dir=None, move_dir=None):
            state['rot_dir'] = rot_dir
            state['move_dir'] = move_dir

        sonars = inp.sonars

        ##### FOR TESTING
        f, r, l = [sonars[s] for s in [F_SONAR, R_SONAR, L_SONAR]]
        print 'Front: {:.2f}, Left: {:.2f}, Right: {:.2f}'.format(f,l,r)
        ##### END FOR TESTING

        closest_sonar, closest_dist = min( enumerate(sonars), key=lambda s: s[1] )

        # middle not in range
        if not in_range(closest_dist):
            return outp()


        # handle alignment
        if closest_sonar == F_SONAR or closest_sonar == L_SONAR:
            set_state('left')
        elif closest_sonar == R_SONAR:
            if too_close(closest_dist):
                set_state('left')
            else:
                set_state(None, 'forward')


        return outp()





mySM = MySMClass()
mySM.name = 'brainSM'

######################################################################
###
###          Brain methods
###
######################################################################

def plotSonar(sonarNum):
    robot.gfx.addDynamicPlotFunction(y=('sonar'+str(sonarNum),
                                        lambda:
                                        io.SensorInput().sonars[sonarNum]))

# this function is called when the brain is (re)loaded
def setup():
    robot.gfx = gfx.RobotGraphics(drawSlimeTrail=False, # slime trails
                                  sonarMonitor=False) # sonar monitor widget

    # set robot's behavior
    robot.behavior = mySM

# this function is called when the start button is pushed
def brainStart():
    robot.behavior.start(traceTasks = robot.gfx.tasks())

# this function is called 10 times per second
def step():
    inp = io.SensorInput()
    # print inp.sonars[3]
    robot.behavior.step(inp).execute()
    io.done(robot.behavior.isDone())

# called when the stop button is pushed
def brainStop():
    pass

# called when brain or world is reloaded (before setup)
def shutdown():
    pass
