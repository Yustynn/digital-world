from helpers import celc

INIT_BOTTLE_TEMP = celc(35)              # (K) system init temp
M_ALGAE = 40.0                           # (g) mass
LAMBDA_ALGAE = 0.055787                  # (W/m^2) surroundings-a]gae transfer
SA_ALGAE = {
    'sun': 0.005524,                     # (m^2) surface area exposed to sun
    'ground': 0.001275,                  # (m^2) surface area exposed to ground
}

C_WATER = 4.184                          # (J/gK) specific heat capacity
MAX_FLOW_RATE = 0.8                      # amt cooling water in pipe (g/s)
T_RESERVOIR = celc(25.0)                # (K) cooling water reservoir temp
