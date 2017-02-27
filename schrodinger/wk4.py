from wk3 import assoc_laguerre, assoc_legendre
from wk2 import to_dp, outp_norm

from sympy import diff, exp, factorial, symbols, simplify
from math import cos, e, pi
import scipy.constants as c

a = c.physical_constants['Bohr radius'][0]

@to_dp(5)
def angular_wave_func(m, l, theta, phi):
    '''
    >>> angular_wave_func(0, 0, 0, 0)
    (0.28209+0j)
    >>> angular_wave_func(1, 1, pi/2, pi)
    (0.34549-0j)
    >>> angular_wave_func(0, 2, pi, 0)
    (0.63078+0j)
    '''
    P_m_l = assoc_legendre(m, l)

    epsilon = (-1)**m if m > 0 else 1

    sqrt_inner_1 = (2*l + 1) / (4*pi)
    sqrt_inner_2 = factorial( l - abs(m) ) / factorial( l + abs(m) )
    sqrt_term = (sqrt_inner_1 * sqrt_inner_2)**0.5

    after_sqrt = e**(1j*m*phi) * P_m_l( theta )

    return complex(epsilon * sqrt_term * after_sqrt, 0j)

@to_dp(5)
@outp_norm(a**-1.5)
def radial_wave_func(n, l, r):
    '''
    >>> radial_wave_func(1, 0, a)
    0.73576
    >>> radial_wave_func(2, 0, a)
    0.12381
    >>> radial_wave_func(2, 1, 2*a)
    0.15019
    >>> radial_wave_func(3, 1, 2*a)
    0.08281
    '''
    p = 2*l + 1
    qmp = n - l - 1

    L_p_qmp = assoc_laguerre(p, qmp)

    term1_sqrt_inner_1          =   (2 / (n*a))**3
    term1_sqrt_inner_2_num      =   factorial(qmp)
    term1_sqrt_inner_2_denom    =   2*n * ( factorial(n + l) )**3
    term1_sqrt_inner_2          =   term1_sqrt_inner_2_num / term1_sqrt_inner_2_denom

    term1 = (term1_sqrt_inner_1 * term1_sqrt_inner_2)**0.5
    term2 = e**(-r / (n*a))
    term3 = (2*r / (n*a))**l
    term4 = L_p_qmp( 2*r / (n*a) )

    return term1 * term2 * term3 * term4

if __name__ == '__main__':
    from doctest import testmod
    testmod()
