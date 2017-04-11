import physics_constants as p

def cooling(power):
    return (power * p.MAX_FLOW_RATE) / (p.C_WATER * M_ALGAE)

def sun(solar_irradiance):
    return solar_irradiance * p.SA_ALGAE['sun']

def surroundings(T, T_sur):
    return p.LAMBDA * (T_sur - T)
