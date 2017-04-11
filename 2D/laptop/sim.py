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
- INDETERMINATE due to conduction between bottle and ground (ground hotter
    -> increase)
- INDETERMINATE due to convection between bottle and surrounding air (air
    hotter -> increase)

Some of our assumptions:
- radiation from the Sun only occurs between 7am btwn 7pm
- the cooling water does not lose heat as it flows through the algae water
'''

from simpy                  import Container
from simpy.rt               import RealtimeEnvironment
from time                   import sleep, strftime
from datetime               import datetime

from sim.EnvConditions      import EnvConditions
from sim.helpers            import celc, hours, mins # unit converters

import sim.delta_Qs          as delta_Qs
import sim.physics_constants as p

# Simpy Config
SIM_TIME         = hours(24)             # seconds
INIT_BOTTLE_TEMP = celc(35)              # (K) system init temp

def logger(process_name, delta_Q, bottle):
    time = strftime('%r')

    print '{}: {} -> {:.2f}J change in heat -> {:.2f}J, {:.2f}K'.format(\
        time, process_name, delta_Q, bottle.heat.level, bottle.temp)

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
    def __init__(self, env, init_temp=INIT_BOTTLE_TEMP):
        heat_amt = init_temp * p.C_WATER * p.M_ALGAE
        self.heat = HeatContainer(env, init=heat_amt)

    @property
    def temp(self):
        return self.heat.level / (p.C_WATER * p.M_ALGAE)

def sun(bottle, env_conds):

    # delta_Q = delta_Qs.sun(env_conds.solar_irradiance)
    delta_Q = delta_Qs.sun(800) # for testing @TODO remove

    logger('sun', delta_Q, bottle)

    yield bottle.heat.delta(delta_Q)

def cooling(bottle, env_conds):
    # delta_Q = delta_Qs.cooling(env_conds.power)
    delta_Q = delta_Qs.cooling(1) # for testing, use max power @TODO remove

    logger('cooling system', delta_Q, bottle)

    yield bottle.heat.delta(delta_Q)

def surroundings(bottle, env_conds):
    delta_Q = delta_Qs.surroundings(bottle.temp, env_conds.temp)

    logger('surroundings', delta_Q, bottle)

    yield bottle.heat.delta(delta_Q)

def print_results(bottle):
    print '\n\nSIMULATION END'
    print 'Time: {}s\nTemperature: {:.2f}\nHeat: {:.2f}\n\n'.format(\
        SIM_TIME, bottle.temp, bottle.heat.level)


def composer(env, bottle, env_conds):
    while True:
        env.process( cooling(bottle, env_conds) )
        env.process( surroundings(bottle, env_conds) )
        if 7 <= datetime.now().hour <= 19:
            env.process( sun(bottle, env_conds) )

        print 'Runtime: {}s \n'.format(env.now)

        if env.now == SIM_TIME - 1:
            print_results(bottle)

        yield env.timeout(1)

env = RealtimeEnvironment(strict=False)
env_conds = EnvConditions()
#
## FOR TESTING ##
from simpy import Environment
env = Environment()
SIM_TIME = hours(5)

bottle = Bottle(env)

env.process( composer(env, bottle, env_conds) )


def start():
    env.run(until=SIM_TIME)

if __name__ == '__main__':
    start()
