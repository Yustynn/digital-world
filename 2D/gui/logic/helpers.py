from threading import Thread

def foreach(f, it):
    for el in it:
        f(el)

def unblock(fn):
    t = Thread(target=fn)
    t.daemon = True
    t.start()
