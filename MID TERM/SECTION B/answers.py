from functools import wraps

# decorator to limit output's dp (handles tuples, lists, complex numbers and numbers)
def to_dp(n):
    def to_dp_wrapper(f):
        @wraps(f)
        def to_dp(*args, **kwargs):
            result = f(*args, **kwargs)

            if isinstance(result, complex):
                return complex( round(result.real, n), round(result.imag, n) )
            if isinstance(result, list):
                return [round(x, n) for x in result]
            if isinstance(result, tuple):
                return tuple(round(x, n) for x in result)

            return round(result, n)

        return to_dp

    return to_dp_wrapper

def ballsdeepmap(f, val):
    if isinstance(val, dict):
        return {k: ballsdeepmap(f, v) for k, v in val.iteritems()}
    elif hasattr(val, '__iter__'):
        return val.__class__( [ballsdeepmap(f, el) for el in val] )
    else:
        return f(val)

def surgery(start, fns):
    operate = lambda v, fn: fn(v)
    return reduce( operate, fns, start )


from math import pi, tan

@to_dp(3)
def area_r_polygon(n, s):
    '''
    >>> area_r_polygon(5, 6.5)
    72.69
    >>> area_r_polygon(7, 3.25)
    38.383
    >>> area_r_polygon(2, 12.5)
    0.0
    '''
    num = n * s**2
    denom = 4 * tan(pi/n)

    return num/denom

def mysum(a, b, limit):
    '''
    >>> mysum(3, 5, 10)
    23
    >>> mysum(2, 4, 12)
    30
    >>> mysum(3, 3, 15)
    30
    >>> mysum(7, 9, 100)
    1266
    >>> mysum(21, 34, 10000)
    3783486
    >>> mysum(0, 5, 10)
    'Wrong input'
    >>> mysum(0.5, 5, 10)
    'Wrong input'
    >>> mysum(3, 'x', 10)
    'Wrong input'
    >>> mysum(2, 3, 0)
    0
    '''
    args = [a, b, limit]

    is_all_int        = all([isinstance(arg, int) for arg in args])
    is_ab_positive    = all([n > 0 for n in [a,b]])

    if not all([is_all_int, is_ab_positive]):
        return 'Wrong input'

    return sum([n for n in range(limit) if (not n%a or not n%b)])




if __name__ == '__main__':
    from doctest import testmod
    testmod()
