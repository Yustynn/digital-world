from math import e, cos

def to_2_dp(f):
    return lambda a, b: round( f(a, b), 2 )

@to_2_dp
def trapezoidal(a, b):
    '''
    >>> trapezoidal(5, 6.5)
    0.13
    >>> trapezoidal(5, 5.5)
    0.03
    >>> trapezoidal(6, 6.5)
    0.07
    >>> trapezoidal(6, 2.5)
    -0.04
    '''
    f = lambda x: cos(x)*e**-2
    return (b - a) * ( f(b) + f(a) )/2

if __name__ == '__main__':
    from doctest import testmod
    testmod()
