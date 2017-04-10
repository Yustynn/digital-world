from threading import Thread

def foreach(f, it):
    for el in it:
        f(el)

def unblock(fn):
    t = Thread(target=fn)
    t.daemon = True
    t.start()

BOLD    = '\e[1m'
BLUE    = '\e[34'
GREEN   = '\e[92m'
RED     = '\e[91m'
YELLOW  = '\e[93m'
RESET   = '\e[0m'

def colorizer_maker(color):
    return lambda str: color + str + RESET

bold, blue, green, red, yellow = map(colorizer_maker, [BOLD, BLUE, GREEN, RED, YELLOW])
