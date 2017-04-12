import physics_constants as p

def cooling(power):
    return -2.4 * power

def sun(solar_irradiance):
    return solar_irradiance * p.SA_ALGAE['sun']

def surroundings(T, T_sur):
    # print 'T: {}, T_sur: {}'.format(T, T_sur)
    return p.LAMBDA_ALGAE * (T_sur - T)
