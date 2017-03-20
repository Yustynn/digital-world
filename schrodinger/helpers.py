### BASE DECORATORS ###

from functools import wraps
import scipy.constants as c

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
    def wrapper(f):
        return lambda *args: f(*args) / n

    return wrapper

def ensure_float_args(f):
    @wraps(f)
    def apply_float_args(*args):
        args = [float(a) for a in args]

        return f(*args)
    return apply_float_args

### ADDITIONAL HELPERS ###

a = c.physical_constants['Bohr radius'][0]

norm_bohr_rad   = norm(a**-1.5)
to_5dp          = to_dp(5)



#### PRINTERS

CYAN  = "\033[1;36m"
GREEN = "\033[1;32m"
RED   = "\033[1;31m"
RESET = "\033[1;0m"

def print_color_generator(C):
    def print_color(*strs):
        print C + ' '.join(strs) + RESET

    return print_color

cyan, green, red = map(print_color_generator, [CYAN, GREEN, RED])
