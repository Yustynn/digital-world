import math
import libdw.util as util
import libdw.sm as sm
import libdw.gfx as gfx
from soar.io import io

from time import sleep

TOLERANCE = 0.01

class MySMClass(sm.SM):
    startState=0
    def getNextValues(self, state, inp):
        f_sonar = inp.sonars[3]
        # print inp.odometry.theta

        print f_sonar

        # goldilocks
        if abs(f_sonar - 0.5) < TOLERANCE:
            return (state, io.Action(fvel = 0, rvel = 0))

        # too cold
        if f_sonar > 0.5 + TOLERANCE:
            return (state, io.Action(fvel = 0.2, rvel = 0))

        # too hot
        if f_sonar < 0.5 - TOLERANCE:
            return (state, io.Action(fvel = -0.2, rvel = 0))

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
    robot.gfx = gfx.RobotGraphics(drawSlimeTrail=True, # slime trails
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
