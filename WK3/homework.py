### PROBLEM 1 ###
def check_value(n1, n2, n3, x):
    '''
    >>> check_value(1,4,7,6)
    True
    >>> check_value(1,4,7,2)
    False
    >>> check_value(100,4,7,50)
    False
    >>> check_value(100,4,7,3)
    False
    >>> check_value(100,4,700,300)
    True
    '''

    return x < n1 and x > n2 and x < n3

### PROBLEM 2 ###
def c_to_f(c):
    return c * 9.0/5 + 32

def f_to_c(f):
    return (f-32) * 5.0/9

def temp_convert(unit, t):
    '''
    Test fahrenheit -> celsius
    >>> temp_convert('C', -40)
    -40.0
    >>> temp_convert('C', 32)
    0.0
    >>> temp_convert('C', 212)
    100.0

    Test celsius -> fahrenheit
    >>> temp_convert('F', 212)
    413.6
    >>> temp_convert('F', 0)
    32.0
    >>> temp_convert('F', -40)
    -40.0

    Test non-existent unit
    >>> temp_convert('auo', 4)
    '''

    map = {
        'F': c_to_f,
        'C': f_to_c
    }

    if unit not in map:
        return None
    else:
        return map[unit](t)

### PROBLEM 3 ###
def get_even_list(l):
    '''Takes in list, returns filtered list with even nums only
    >>> get_even_list([1 ,2 ,3 ,4 ,5])
    [2, 4]
    >>> get_even_list([10 ,20 ,30 ,40 ,50])
    [10, 20, 30, 40, 50]
    >>> get_even_list([11 ,21 ,31 ,41 ,51])
    []
    '''
    return [n for n in l if n % 2 == 0]

def is_prime(n):
    '''
    >>> is_prime(2)
    True
    >>> is_prime(3)
    True
    >>> is_prime(7)
    True
    >>> is_prime(9)
    False
    >>> is_prime(21)
    False
    '''
    # really bad, inefficient code below, but it's fun
    return not any([d for d in xrange(2, n) if n % d == 0]) and n > 1

### PROBLEM 5 ###

from math import e

def to_three_dp(f):
    return lambda *args: round( f(*args), 3 )


# tests aren't being run. Why? Because decorated?
# You may be asking yourself, why the reduce in this case? Doesn't it just
# convolute things? Wouldn't a while loop be better? The answer is simple: yes.
@to_three_dp
def approx_ode(h, t0, y0, t):
    '''
    >>> approx_ode(0.1, 0, 1, 3)
    5.292
    >>> approx_ode(0.1, 0, 1, 4)
    5.601
    >>> approx_ode(0.1, 0, 1, 5)
    5.771
    >>> approx_ode(0.1, 0, 1, 2.5)
    5.045
    '''

    steps_per_unit = int(1/h)
    t_limit = int(t*steps_per_unit)

    f = lambda n, y: 3 + e**-n - 0.5*y
    y_next = lambda y_n, f: y_n + h*f

    def y_iterator(y_n, i):
        t_n = i*h
        return y_next( y_n, f(t_n, y_n) )

    return reduce(y_iterator, xrange(0, t_limit), 1)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
