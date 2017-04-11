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
BLUE    = "\033[0;34m"
GREEN   = "\033[0;32m"
RED     = "\033[0;31m"
YELLOW  = "\033[0;33m"
RESET   = "\033[0m"

YELLOW_BOLD = "\033[1;33m"

def colorizer_maker(color):
    return lambda str: color + str + RESET

blue, green, red, yellow = map(colorizer_maker, [BLUE, GREEN, RED, YELLOW])

yellow_bold = colorizer_maker(YELLOW_BOLD)

# unit converters
celc = lambda c: c + 273.15 # degC to K
mins = lambda m: m * 60 # min to s
hours = lambda h: mins(h * 60) # hours to s
