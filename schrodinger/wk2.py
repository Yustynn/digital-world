from functools import wraps

### HELPERS ###

# decorator to limit dp (handles tuples, lists, and numbers)
def to_dp(n):
    def to_dp_wrapper(f):
        @wraps(f)
        def to_dp(*args, **kwargs):
            result = f(*args, **kwargs)

            if isinstance(result, tuple):
                return tuple(round(x, n) for x in result)
            if isinstance(result, list):
                return [round(x, n) for x in result]
            return round(result, n)

        return to_dp

    return to_dp_wrapper

def ensure_float_args(f):
    @wraps(f)
    def apply_float_args(*args):
        args = [float(a) for a in args]

        return f(*args)
    return apply_float_args

### STARTING PROPER ###
import numpy as np
import scipy.constants as c
from numpy import sin, cos, arctan, sign

### Question 1 ###

@to_dp(5)
def energy_n(n):
    '''
    >>> energy_n(1)
    -13.60569
    >>> energy_n(2)
    -3.40142
    >>> energy_n(3)
    -1.51174
    '''

    e         = c.e
    epsilon_0 = c.epsilon_0
    h         = c.h, m_e, = c.e, c.epsilon_0, c.h, c.m_e
    e_v = c.physical_constants['electron volt'](0)

    return (-e**4 * m_e) / (8 * epsilon_0 * n**2 * h**2)




### Question 2 ###
@ensure_float_args
@to_dp(5)
def deg_to_rad(d):
    '''
    >>> deg_to_rad(90)
    1.5708
    >>> deg_to_rad(180)
    3.14159
    >>> deg_to_rad(270)
    4.71239
    '''

    return d * np.pi / 180


@ensure_float_args
@to_dp(5)
def rad_to_deg(r):
    '''
    >>> rad_to_deg(3.14)
    179.90875
    >>> rad_to_deg(3.14/2.0)
    89.95437
    >>> rad_to_deg(3.14*3/4)
    134.93156
    '''

    return r / np.pi * 180

### Question 3 ###
@ensure_float_args
@to_dp(5)
def spherical_to_cartesian(r, theta, phi):
    '''
    >>> spherical_to_cartesian(3,0,np.pi)
    (-0.0, 0.0, 3.0)
    >>> spherical_to_cartesian(3,np.pi/2.0,np.pi/2.0)
    (0.0, 3.0, 0.0)
    >>> spherical_to_cartesian(3,np.pi, 0)
    (0.0, 0.0, -3.0)
    '''
    x = r*sin(theta)*cos(phi)
    y = r*sin(theta)*sin(phi)
    z = r*cos(theta)
    return x, y, z

@ensure_float_args
@to_dp(5)
def cartesian_to_spherical(x, y, z):
    '''
    >>> cartesian_to_spherical(3,0,0)
    (3.0, 1.5708, 0.0)
    >>> cartesian_to_spherical(0,3,0)
    (3.0, 1.5708, 1.5708)
    >>> cartesian_to_spherical(0,0,3)
    (3.0, 0.0, 0.0)
    >>> cartesian_to_spherical(0,-3,0)
    (3.0, 1.5708, -1.5708)
    '''

    # pythagoras' theorem
    get_hyp = lambda a, b: (a**2 + b**2)**0.5

    x_y_hyp = get_hyp(x, y)

    r = get_hyp(x_y_hyp, z)
    if x == 0:
        phi = 90 * sign(y)
    else:
        phi = arctan(y/x)

    if z == 0:
        theta = 90
    else:
        theta = arctan(x_y_hyp / z)

    return r, deg_to_rad(theta), deg_to_rad(phi)

if __name__ == '__main__':
    from doctest import testmod
    testmod()
