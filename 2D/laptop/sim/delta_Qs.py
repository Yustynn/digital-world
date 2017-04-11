import physics_constants as p

def cooling(power):
    # power *= 6 * 0.25 # assume 6V power supply, 0.25A current

    return -2.4 * power
    # return -(power * p.MAX_FLOW_RATE) / (p.C_WATER * p.M_ALGAE)

def sun(solar_irradiance):
    return solar_irradiance * p.SA_ALGAE['sun']

def surroundings(T, T_sur):
    return p.LAMBDA_ALGAE * (T_sur - T)
