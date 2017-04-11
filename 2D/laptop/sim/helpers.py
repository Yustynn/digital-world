from threading import Thread

# map isn't quite right a lot of the time
def foreach(f, it):
    for el in it:
        f(el)

# run fn in new thread
def unblock(fn):
    t = Thread(target=fn)
    t.daemon = True
    t.start()

# string formatters
BOLD    = '\e[1m'
BLUE    = '\e[34'
GREEN   = '\e[92m'
RED     = '\e[91m'
YELLOW  = '\e[93m'
RESET   = '\e[0m'

def colorizer_maker(color):
    return lambda str: color + str + RESET

bold, blue, green, red, yellow = map(colorizer_maker, [BOLD, BLUE, GREEN, RED, YELLOW])

# unit converters
celc = lambda c: c + 273.15 # degC to K
mins = lambda m: m * 60 # min to s
hours = lambda h: mins(h * 60) # hours to s
