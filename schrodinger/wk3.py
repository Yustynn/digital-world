from sympy import diff, exp, factorial, symbols
from math import cos, isnan

def assoc_legendre(m_val, l_val):
    '''
    >>> assoc_legendre(0,0)(1)
    1.00000000000000
    >>> assoc_legendre(1,1)(1)
    0.841470984807896
    >>> assoc_legendre(2,3)(1)
    5.73860550925719
    >>> assoc_legendre(2,3)(0)
    0.0
    '''
    m, l, x = symbols('m l x')

    def P_l():
        term1 = 1 / ( 2**l * factorial(l) )
        term2 = diff( (x**2 - 1)**l, x, l_val )

        return term1 * term2

    def legendre(theta_val):
        x_val = cos(theta_val)

        term1 = ( 1 - x**2 )**( abs(m)/ 2 )
        term2 = diff( P_l(), x, abs(m_val) )

        ans_expr = term1 * term2

        ans_val = ans_expr.subs({
            m: 1.*m_val,
            l: 1.*l_val,
            x: 1.*x_val
        })


        return 0.0 if isnan(ans_val) else ans_val # I'm a haxx0r

    return legendre

def assoc_laguerre(p_val, qmp_val):
    '''
    >>> assoc_laguerre(0,0)(1)
    1
    >>> assoc_laguerre(1,1)(1)
    2
    >>> assoc_laguerre(2,2)(1)
    60
    >>> assoc_laguerre(2,2)(0)
    144
    '''
    q_val = qmp_val + p_val
    p, q, x = symbols('p q x')

    def L_q():
        term1 = exp(x)

        term2_expr = exp(-x) * x**q_val
        term2 = diff( term2_expr, x, q_val )

        return term1 * term2

    def laguerre(x_val):
        vals = {
            p: p_val,
            q: q_val,
            x: x_val
        }

        term1 = (-1)**p
        term2 = diff( L_q(), x, p_val )

        ans_expr = term1 * term2

        return ans_expr.subs(vals)

    return laguerre

if __name__ == '__main__':
    from doctest import testmod
    testmod()
