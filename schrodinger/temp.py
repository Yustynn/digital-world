import numpy as np
import scipy.constants as c
from sympy import diff, exp, factorial, symbols, simplify, pprint
from math import cos, e, pi, isnan

from functools import wraps


import functools
from collections import namedtuple
from threading import RLock

_CacheInfo = namedtuple("CacheInfo", ["hits", "misses", "maxsize", "currsize"])


@functools.wraps(functools.update_wrapper)
def update_wrapper(wrapper,
                   wrapped,
                   assigned = functools.WRAPPER_ASSIGNMENTS,
                   updated = functools.WRAPPER_UPDATES):
    """
    Patch two bugs in functools.update_wrapper.
    """
    # workaround for http://bugs.python.org/issue3445
    assigned = tuple(attr for attr in assigned if hasattr(wrapped, attr))
    wrapper = functools.update_wrapper(wrapper, wrapped, assigned, updated)
    # workaround for https://bugs.python.org/issue17482
    wrapper.__wrapped__ = wrapped
    return wrapper


class _HashedSeq(list):
    __slots__ = 'hashvalue'

    def __init__(self, tup, hash=hash):
        self[:] = tup
        self.hashvalue = hash(tup)

    def __hash__(self):
        return self.hashvalue


def _make_key(args, kwds, typed,
              kwd_mark=(object(),),
              fasttypes=set([int, str, frozenset, type(None)]),
              sorted=sorted, tuple=tuple, type=type, len=len):
    'Make a cache key from optionally typed positional and keyword arguments'
    key = args
    if kwds:
        sorted_items = sorted(kwds.items())
        key += kwd_mark
        for item in sorted_items:
            key += item
    if typed:
        key += tuple(type(v) for v in args)
        if kwds:
            key += tuple(type(v) for k, v in sorted_items)
    elif len(key) == 1 and type(key[0]) in fasttypes:
        return key[0]
    return _HashedSeq(key)


def lru_cache(maxsize=100, typed=False):
    """Least-recently-used cache decorator.

    If *maxsize* is set to None, the LRU features are disabled and the cache
    can grow without bound.

    If *typed* is True, arguments of different types will be cached separately.
    For example, f(3.0) and f(3) will be treated as distinct calls with
    distinct results.

    Arguments to the cached function must be hashable.

    View the cache statistics named tuple (hits, misses, maxsize, currsize) with
    f.cache_info().  Clear the cache and statistics with f.cache_clear().
    Access the underlying function with f.__wrapped__.

    See:  http://en.wikipedia.org/wiki/Cache_algorithms#Least_Recently_Used

    """

    # Users should only access the lru_cache through its public API:
    #       cache_info, cache_clear, and f.__wrapped__
    # The internals of the lru_cache are encapsulated for thread safety and
    # to allow the implementation to change (including a possible C version).

    def decorating_function(user_function):

        cache = dict()
        stats = [0, 0]                  # make statistics updateable non-locally
        HITS, MISSES = 0, 1             # names for the stats fields
        make_key = _make_key
        cache_get = cache.get           # bound method to lookup key or return None
        _len = len                      # localize the global len() function
        lock = RLock()                  # because linkedlist updates aren't threadsafe
        root = []                       # root of the circular doubly linked list
        root[:] = [root, root, None, None]      # initialize by pointing to self
        nonlocal_root = [root]                  # make updateable non-locally
        PREV, NEXT, KEY, RESULT = 0, 1, 2, 3    # names for the link fields

        if maxsize == 0:

            def wrapper(*args, **kwds):
                # no caching, just do a statistics update after a successful call
                result = user_function(*args, **kwds)
                stats[MISSES] += 1
                return result

        elif maxsize is None:

            def wrapper(*args, **kwds):
                # simple caching without ordering or size limit
                key = make_key(args, kwds, typed)
                result = cache_get(key, root)   # root used here as a unique not-found sentinel
                if result is not root:
                    stats[HITS] += 1
                    return result
                result = user_function(*args, **kwds)
                cache[key] = result
                stats[MISSES] += 1
                return result

        else:

            def wrapper(*args, **kwds):
                # size limited caching that tracks accesses by recency
                key = make_key(args, kwds, typed) if kwds or typed else args
                with lock:
                    link = cache_get(key)
                    if link is not None:
                        # record recent use of the key by moving it to the front of the list
                        root, = nonlocal_root
                        link_prev, link_next, key, result = link
                        link_prev[NEXT] = link_next
                        link_next[PREV] = link_prev
                        last = root[PREV]
                        last[NEXT] = root[PREV] = link
                        link[PREV] = last
                        link[NEXT] = root
                        stats[HITS] += 1
                        return result
                result = user_function(*args, **kwds)
                with lock:
                    root, = nonlocal_root
                    if key in cache:
                        # getting here means that this same key was added to the
                        # cache while the lock was released.  since the link
                        # update is already done, we need only return the
                        # computed result and update the count of misses.
                        pass
                    elif _len(cache) >= maxsize:
                        # use the old root to store the new key and result
                        oldroot = root
                        oldroot[KEY] = key
                        oldroot[RESULT] = result
                        # empty the oldest link and make it the new root
                        root = nonlocal_root[0] = oldroot[NEXT]
                        oldkey = root[KEY]
                        root[KEY] = root[RESULT] = None
                        # now update the cache dictionary for the new links
                        del cache[oldkey]
                        cache[key] = oldroot
                    else:
                        # put result in a new link at the front of the list
                        last = root[PREV]
                        link = [last, root, key, result]
                        last[NEXT] = root[PREV] = cache[key] = link
                    stats[MISSES] += 1
                return result

        def cache_info():
            """Report cache statistics"""
            with lock:
                return _CacheInfo(stats[HITS], stats[MISSES], maxsize, len(cache))

        def cache_clear():
            """Clear the cache and cache statistics"""
            with lock:
                cache.clear()
                root = nonlocal_root[0]
                root[:] = [root, root, None, None]
                stats[:] = [0, 0]

        wrapper.__wrapped__ = user_function
        wrapper.cache_info = cache_info
        wrapper.cache_clear = cache_clear
        return update_wrapper(wrapper, user_function)

    return decorating_function






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

def norm(n):
    def norm_wrapper(f):
        return lambda *args: f(*args) / n

    return norm_wrapper

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

    e           = c.e
    epsilon_0   = c.epsilon_0
    h_bar       = c.hbar
    m_e         = c.m_e
    pi          = c.pi

    e_v         = c.physical_constants['electron volt'][0]

    term1 = m_e / (2 * h_bar**2)
    term2 = e**2 / (4 * pi * epsilon_0)
    term3 = n**-2

    joules = - term1 * (term2**2) * term3

    return joules / e_v


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


@lru_cache(maxsize=320)
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

        # without simplify, nan'd out
        return simplify(term1 * term2)

    def legendre(theta_val):
        x_val = cos(theta_val)

        term1 = ( 1 - x**2 )**( abs(m)/ 2 )
        term2 = diff( P_l(), x, abs(m_val) )
        ans_expr = simplify(term1 * term2)

        ans_val = ans_expr.subs({
            m: m_val,
            l: l_val,
            x: x_val
        })

        return ans_val

    return legendre

@lru_cache(maxsize=320)
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

        return simplify(term1 * term2)

    def laguerre(x_val):
        vals = {
            p: p_val,
            q: q_val,
            x: x_val
        }

        term1 = (-1)**p
        term2 = diff( L_q(), x, p_val )

        ans_expr = simplify(term1 * term2)

        return ans_expr.subs(vals)

    return laguerre


a = c.physical_constants['Bohr radius'][0]

@lru_cache(maxsize=320)
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

@lru_cache(maxsize=320)
@to_dp(5)
@norm(a**-1.5)
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
    term1_sqrt_inner_2_denom    =   2*n * ( factorial(n+l) )**3
    term1_sqrt_inner_2          =   term1_sqrt_inner_2_num / term1_sqrt_inner_2_denom

    term1 = (term1_sqrt_inner_1 * term1_sqrt_inner_2)**0.5
    term2 = e**(-r / (n*a))
    term3 = (2*r / (n*a))**l
    term4 = L_p_qmp( 2*r / (n*a) )

    return term1 * term2 * term3 * term4

@lru_cache(maxsize=320)
def hydrogen_wave_func(n, l, m, r_max, *n_xyz):
    x, y, z = [np.linspace(-r_max, r_max, n_dim) for n_dim in n_xyz]
    cartesian_mesh   = np.meshgrid(x, y, z)

    r3, theta3, phi3 = np.vectorize(cartesian_to_spherical)(*cartesian_mesh)
    r3              *= a

    ang_func, rad_func = map(np.vectorize, [angular_wave_func, radial_wave_func])
    ang_mag,  rad_mag  = ang_func(m,l,theta3,phi3), rad_func(n,l,r3)

    density = np.absolute(ang_mag*rad_mag)**2
    density = np.round(density)

    return tuple([np.round(arr) for arr in (tuple(cartesian_mesh) + (density,))])
