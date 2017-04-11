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
- INDETERMINATE due to conduction between bottle and ground (depends on
 temperature)
- INDETERMINATE due to convection between bottle and surrounding air (depends
 on temperature)

For simplicity, we make the following assumptions:
- radiation from the Sun only occurs between 7am btwn 7pm
- the cooling water does not lose heat as it flows through the algae water
- 
'''

from simpy          import Container
from simpy.rt       import RealtimeEnvironment
from time           import strftime
from datetime       import datetime

from EnvConditions  import EnvConditions
from helpers        import celc, hours, mins # unit converters
from State          import state

import delta_Qs
import physics_constants as p

env_conds = EnvConditions()

# Simpy Config
SIM_TIME         = hours(8) + mins(30)   # seconds
INIT_BOTTLE_TEMP = celc(35)              # (K) system init temp

env = RealtimeEnvironment(strict=False)

## FOR TESTING ##
# from simpy import Environment
# env = Environment()
# SIM_TIME = 10

def logger(process_name, delta_Q, bottle):
    time = strftime('%r')

    print '{}: {} -> {:.2f}J change in heat -> {}J, {}K'.format(\
        time, process_name, delta_Q, bottle.temp)

class HeatContainer(Container):
    def init(self, **kwargs):
        Container.__init__(self, **kwargs)

    # often don't know if the heat is additive or subtractive. This can take either
    def delta(self, amt):
        if amt > 0:
            return self.put(amt)

        return self.get(-amt)

class Bottle(object):
    def __init__(self, env, init_temp=INIT_BOTTLE_TEMP):
        heat_amt = init_temp * p.C_WATER * p.M_ALGAE
        self.heat = HeatContainer(env, init=heat_amt)

    @property
    def temp(self):
        self.heat.level / (p.C_WATER * p.M_ALGAE)

def sun(bottle, env_conds):
    delta_Q = delta_Qs['sun'](env_conds.solar_irradiance)

    logger('sun', delta_Q, bottle)

    yield bottle.heat.delta(delta_Q)

def cooling(bottle, state):
    delta_Q = delta_Qs['cooling'](state.power)

    logger('cooling system', delta_Q, bottle)

    yield bottle.heat.delta(delta_Q)

def surroundings(bottle, env_conds):
    delta_Q = delta_Qs['surroundings'](bottle.temp, env_conds.temp)

    logger('surroundings', delta_Q, bottle)

    yield bottle.heat.delta(delta_Q)

def composer(env, bottle, env_conds, state):
    while True:
        env.process( cooling(bottle, state) )
        env.process( surroundings(bottle, env_conds) )
        
        if 7 <= datetime.now().hour <= 19:
            env.process( sun(bottle, env_conds) )

        yield env.timeout(1)

env.process( composer(env, bottle, env_conds, state) )

def start():
    env.run(until=SIM_TIME)

if __name__ == '__main__':
    start()
