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

For simplicity, we assume that radiation from the Sun is constant between 7am
and 7pm, and that there is no radiation from the Sun otherwise.
'''

from simpy          import Container
from simpy.rt       import RealtimeEnvironment
from datetime       import datetime

from EnvConditions  import EnvConditions

env_conds = EnvConditions()

# Helpers to more semantically express time in seconds
mins  = lambda m: m*60
hours = lambda h: mins(h*60)

# celcius -> kelvin
celcius = lambda c: c + 273.15

# Simpy Config
SIM_TIME         = hours(8) + mins(30)   # seconds
INIT_TEMP        = celcius(35)           # (K) system init temp
RESERVOIR_TEMP   = celcius(25)           # (K) reservoir constant temp
RAD_SUN          = 4000                  # heat from Sun (watts)

# Physics Constants (for computation)
BOTTLE_LAMBD     = 0.5                  # conductivity^-1
BOTTLE_AIR_SA    = 0.05                 # (m^2) bottle surface area exposed to air
BOTTLE_GROUND_SA = 0.02                 # (m^2) bottle surface area exposed to ground
ALGAE_MASS       = 40                    # g
ALGAE_C          = 4.184                 # J/gK

env = RealtimeEnvironment(strict=False)

## FOR TESTING ##
# from simpy import Environment
# env = Environment()
# SIM_TIME = 10

class HeatContainer(Container):
    def init(self, **kwargs):
        Container.__init__(self, **kwargs)

    # we often don't know if the heat is additive or subtractive. This can take either
    def add(self, amt):
        if amt > 0:
            return self.put(amt)

        return self.get(-amt)

class Bottle(object):
    '''
    Bottle houses algae (in water)
    Algae, bottle and water all seen as a single system

    Heat transfer with surrounding air
    '''

    def __init__(self):
        heat_val = self.temp_to_heat(INIT_TEMP)

        self.env        = env
        self.heat       = HeatContainer(env, init=heat_val)
        self.lambd      = BOTTLE_LAMBD

        self.sa = {
            'air':    BOTTLE_AIR_SA,
            'ground': BOTTLE_GROUND_SA
        }

    @property
    def temp(self):
        return self.heat_to_temp(self.heat.level)
        
    def heat_to_temp(self, heat):
        return heat / (ALGAE_MASS * ALGAE_C) 

    def temp_to_heat(self, temp):
        return temp * (ALGAE_MASS * ALGAE_C) 

    def convection(self, h, A, T_sur):
        delta_T = self.temp - T_sur

        delta_Q = -(h * A * delta_T) # for 1s

        print 'Convection removing {} at {}'.format(delta_Q, datetime.now())

        return self.heat.add(delta_Q)

    def conduction(self, T_sur):
        lambd   = self.lambd
        delta_T = self.temp - T_sur

        delta_Q = -(lambd * delta_T) # for 1s

        print 'Conduction removing {} at {}'.format(delta_Q, datetime.now())

        return self.heat.add(delta_Q)
        
def sun(env, bottle):
    yield bottle.heat.add(RAD_SUN)

def surr_air(env, bottle, env_conds):
    T_sur = env_conds.temp
    v     = env_conds.wind_vel
    
    # using Watmuff's amendment to Jurges' eqn
    # source: https://c.ymcdn.com/sites/www.saimeche.org.za/resource/collection/A9416D0D-99A6-4534-B5C5-15E8475524FE/Kr_ger-2002_01__600_dpi_-_2002__18_3___49-54.pdf
    h = 2.8 + 3*v

    yield bottle.convection(h, bottle.sa['air'], T_sur)

# @TODO: Fix conduction to take in different lambda for this one
def ground(env, bottle, env_conds):
    T_sur = env_conds.temp

    yield bottle.conduction(T_sur)

def water(env, bottle):
    T_sur = RESERVOIR_TEMP

    print 'WATER:'
    yield bottle.conduction(T_sur)

def composer(env, bottle):
    while 1:
        if 7 <= datetime.now().hour <= 19:
            env.process(sun(env, bottle))
        env.process(surr_air(env, bottle, env_conds))
        env.process(ground(env, bottle, env_conds))
        print '{:.2f}K temperature!'.format(bottle.temp)
        yield env.timeout(1)

bottle = Bottle()
env.process( composer(env, bottle) )
env.run(until=SIM_TIME)
