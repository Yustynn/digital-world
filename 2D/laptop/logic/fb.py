from firebase    import firebase
from os          import environ as env
from collections import namedtuple

URL    = env['T3_2D_DB_URL']
SECRET = env['T3_2D_DB_SECRET']
fb = firebase.FirebaseApplication(URL, SECRET)

get = lambda key: float( fb.get('/'+key) )
set = lambda key, val: fb.put('/', key, val)
