from sympy import diff, exp, factorial, symbols, init_printing
from wk2 import deg_to_rad

init_printing(use_unicode=True)

def assoc_legendre(m_val, l_val):
    m, l, x = symbols('m l x')

    def P_l():
        term1 = 1 / ( 2**l * factorial(l) )
        term2 = diff( (x**2 - 1)**l, x, l_val )
        
        return term1 * term2
    
    def legendre(x_val):
        term1 = ( 1 - x**2 )**( abs(m)/ 2 )
        term2 = diff( P_l(), x, abs(m_val) )

        ans_expr = term1 * term2
        
        print '\n'
        print P_l(), P_l().subs({
            x: 1.*x_val,
            l: 1.*l_val
        })

        return ans_expr.subs({
            m: 1.*m_val,
            l: 1.*l_val,
            x: 1.*x_val
        })

    return legendre

#print assoc_legendre(0,0)(1)
#print assoc_legendre(1,1)(1)
#print assoc_legendre(2,3)(1)
#print assoc_legendre(2,3)(0)

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
