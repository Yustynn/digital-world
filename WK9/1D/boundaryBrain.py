import math
import libdw.util as util
import libdw.sm as sm
import libdw.gfx as gfx
from soar.io import io

###### CONSTANTS #######
# Dist-related
DIST          = 0.4
TOLERANCE     = 0.05
ADJ_TOLERANCE = 0.03

# Movement-related
TRANS_MAG  = 0.4
ROT_MAG    = 0.4

# Sensor-related
F_SONAR = 2
R_SONARS = 4,

# State modes
ADJUST_LEFT  = 'adjust left'
ADJUST_RIGHT = 'adjust right'
FOLLOWING    = 'following'
SEEKING      = 'seeking'
START        = 'start'


# HELPERS
# Distance-related in general
def in_range(d):  return d - DIST < TOLERANCE
def too_close(d): return d < DIST - TOLERANCE
def too_far(d):   return d > DIST

# Distance-related for adjusting to stay in range
def in_adj_range(d): return DIST - d < ADJ_TOLERANCE

count = 0 # for testing

class MySMClass(sm.SM):
    startState = { 'mode': START }

    def getNextValues(self, state, inp):
        # SEMANTIC MOVEMENT HELPERS
        # turn
        def fleft():    return state, io.Action(fvel =  TRANS_MAG,   rvel =  ROT_MAG/2)
        def fright():   return state, io.Action(fvel =  TRANS_MAG,   rvel = -ROT_MAG/2)
        def bleft():    return state, io.Action(fvel = -TRANS_MAG,   rvel =  ROT_MAG/2)
        def bright():   return state, io.Action(fvel = -TRANS_MAG,   rvel = -ROT_MAG/2)
        # forward
        def forward():  return state, io.Action(fvel =  TRANS_MAG,   rvel = 0)
        def backward(): return state, io.Action(fvel = -TRANS_MAG,   rvel = 0)
        def turn():     return state, io.Action(fvel =  0,           rvel = ROT_MAG)

        sonars = inp.sonars

        # closest sonar and distance respectively
        c_sonar, c_dist = min( enumerate(sonars), key=lambda s: s[1] )
        c_sonar_is_r = c_sonar in R_SONARS


        ##### FOR TESTING
        global count
        count += 1
        f, r, l = [sonars[s] for s in [2, 4, 0]]

        print '{:^40}'.format('ITERATION ' + str(count))
        print 'Front: {:.2f}, Left: {:.2f}, Right: {:.2f}'.format(f,l,r)
        print 'State: {}'.format(state['mode'])
        print 'Closest Dist: {}, Closest Sonar: {}'.format(c_dist, c_sonar)
        print 'In range: {}'.format(in_range(c_dist))
        print '\n'
        ##### END FOR TESTING

        mode = state['mode'] # for convenience

        if mode == START:
            if not in_range(c_dist): # we actually want it a little too close
                return forward()

            state['mode'] = SEEKING
            return turn()

        if mode == SEEKING:
            if c_sonar_is_r:
                state['mode'] = FOLLOWING
                return forward()

            if too_close(c_dist) and c_sonar == F_SONAR:
                print 'close leh, go back'
                return backward()

            return turn()

        if mode == FOLLOWING:
            if not in_range(c_dist) or not c_sonar_is_r:
                state['mode'] = SEEKING
                return turn()

            if too_close(c_dist):
                print 'close leh, changing to adjusting'
                state['mode'] = ADJUST_LEFT
                return fleft()

            if too_far(c_dist):
                print 'far leh, changing to adjusting'
                state['mode'] = ADJUST_RIGHT
                return fright()

            return forward()

        if mode == ADJUST_LEFT:
            if in_adj_range(c_dist):
                state['mode'] = FOLLOWING
                return forward()
            return fleft()

        if mode == ADJUST_RIGHT:
            if in_adj_range(c_dist):
                state['mode'] = FOLLOWING
                return forward()
            return fright()


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
