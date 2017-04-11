from helpers import celc

C_WATER = 4.184 # J/gK
M_ALGAE = 40.0    # g
SA_ALGAE = {    # m^2
    'sun': 0.005524,
    'ground': 0.001275,
}

LAMBDA_ALGAE = 0.055787 # surroundings-a]gae (W/m^2)
MAX_FLOW_RATE = 0.8 # of cooling water in pipe (g/s)
# MAX_FLOW_RATE = 400 # of cooling water in pipe (g/s)
T_RESERVOIR = celc(25.0) # cooling water reservoir temp (K)
#
# 5 degrees c in 4 mins
#
# 1.25K / min
#
# 0.02K / s

# 0.02K * C_WATER * M_ALGAE
