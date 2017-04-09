from firebase    import firebase
from os          import environ as env
from collections import namedtuple

URL    = env['T3_2D_DB_URL']
SECRET = env['T3_2D_DB_SECRET']
fb = firebase.FirebaseApplication(URL, SECRET)

get = lambda key: float( fb.get('/'+key) )
set = lambda key, val: fb.put('/', key, val)

from time import sleep

START = 34
END   = 29
STEPS = 50

incr = (END - START)/(STEPS-1.)

for i in range(STEPS):
    temp = START + incr*(i+1)
    set('temp', temp)
    print 'temp set to {}'.format(temp)
