from threading import Thread

from constants import TEST_LOG, LOG

# unobstructs the main thread
def unblock(fn):
    t = Thread(target=fn)
    t.daemon = True
    t.start()

## STRING FORMATTERS
def colorizer_maker(color):
    RESET   = "\033[0m"
    return lambda val: color + str(val) + RESET

colorbase = {
    'blue':   "\033[0;34m",
    'bluebg': "\033[44m",
    'gray':   "\033[1;30m",
    'green':  "\033[0;32m",
    'red':    "\033[0;31m",
    'redbg':  "\033[41m",
    'yellow': "\033[0;33m"
}

colorizers = {color: colorizer_maker(code) for color, code in colorbase.iteritems()}
## LOGGERS
# prints actual logs
def log(*args, **kwargs):
    if LOG:
        color = kwargs.get('color', None)
        for arg in args:
            if colorizers.get(color, None):
                print colorizers[color](arg)
            else:
                print arg

# prints test logs
def tlog(color=None, *args):
    if TEST_LOG:
        color = kwargs.get('color', None)
        for arg in args:
            if colorizers.get(color, None):
                print colorizers[color](arg)
            else:
                print arg
