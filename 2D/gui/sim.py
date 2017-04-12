'''
We're trying to keep algae (bottled with water) at a constant temperature by
using a variable flow water cooling system.

This HILS pulls real data about current environmental temperature
and wind speed in order to more accurately simulate actual processes of heat
transfer.

One requirement was to distinguish between processes that increase system
temperature and those which decrease it. To that end:
- INCREASE due to radiation from SUN
- DECREASE due to convection with water cooling
- INDETERMINATE due to convection between bottle and surrounding air (air
    hotter -> increase)

Some of our assumptions:
- radiation from the Sun only occurs between 7am btwn 7pm
- the cooling water does not lose heat as it flows through the algae water
'''

# simpy mods / python core mods
from simpy                  import Container
from simpy.rt               import RealtimeEnvironment
from time                   import sleep, strftime
from datetime               import datetime

# custom mods
from sim_scripts.SimState   import SimState
from sim_scripts.helpers    import celc, hours, mins # unit converters
from sim_scripts.helpers    import red, green, blue  # string colorizers

import sim_scripts.delta_Qs          as delta_Qs
import sim_scripts.physics_constants as p

# Simpy Config
IS_LOG_ON        = True                  # Print useful informaion every iteration
IS_FAST_MODE     = False                 # Use non real-time environment
SIM_TIME         = hours(24)             # (s)

def logger(process_name, delta_Q, bottle, colorizer=None):
    if IS_LOG_ON:
        time = strftime('%r')
        text = '{}: {:15} -> {:5.2f}J change in heat -> {:.2f}J, {:.2f}K'.format(\
            time, process_name, delta_Q, bottle.heat.level, bottle.temp)

        if colorizer:
            text = colorizer(text)
        print text

def print_results(bottle):
    print '\n\nSIMULATION END'
    print 'Time: {}s\nTemperature: {:.2f}\nHeat: {:.2f}\n\n'.format(\
        SIM_TIME, bottle.temp, bottle.heat.level)

class HeatContainer(Container):
    def init(self, **kwargs):
        Container.__init__(self, **kwargs)

    # often don't know if the heat is additive or subtractive. This can take either
    def delta(self, amt):
        if not amt:
            amt = 0.01

        if amt >= 0:
            return self.put(amt)

        return self.get(-amt)

class Bottle(object):
    def __init__(self, env, init_temp=p.INIT_BOTTLE_TEMP):
        heat_amt = init_temp * p.C_WATER * p.M_ALGAE
        self.heat = HeatContainer(env, init=heat_amt)

    @property
    def temp(self):
        return self.heat.level / (p.C_WATER * p.M_ALGAE)

### HEAT TRANSFER PROCESSES (not simpy processes) ###
def sun(bottle, sim_state):
    delta_Q = delta_Qs.sun(sim_state.solar_irradiance)

    logger('sun', delta_Q, bottle, red)

    yield bottle.heat.delta(delta_Q)

def cooling(bottle, sim_state):
    delta_Q = delta_Qs.cooling(sim_state.power)

    # log power consumed
    sim_state.power_consumed += sim_state.power * p.MAX_POWER

    logger('cooling system', delta_Q, bottle, blue)

    yield bottle.heat.delta(delta_Q)

def surroundings(bottle, sim_state):
    delta_Q = delta_Qs.surroundings(bottle.temp, sim_state.temp)

    logger('surroundings', delta_Q, bottle, green)

    yield bottle.heat.delta(delta_Q)

### DEFINE PROCESSES ###
# runs all heat-processes once per second
def conductor(env, bottle, sim_state):
    while True:
        env.process( cooling(bottle, sim_state) )
        env.process( surroundings(bottle, sim_state) )
        if 7 <= datetime.now().hour <= 19:
            env.process( sun(bottle, sim_state) )

        if IS_LOG_ON:
            print '{:^75}'.format( 'SIMTIME: {}s \n'.format(env.now) )

        if env.now == SIM_TIME - 1:
            print_results(bottle)

        yield env.timeout(1)

### CONFIG SIM ###
if IS_FAST_MODE:
    from simpy import Environment
    env = Environment()
else:
    env = RealtimeEnvironment(strict=False)

sim_state = SimState()
bottle = Bottle(env)

### REGISTER ALL PROCESSES ###
env.process( conductor(env, bottle, sim_state) )

# If running from GUI, we want to start the sim in a different thread
def start():
    env.run(until=SIM_TIME)

if __name__ == '__main__':
    start()
