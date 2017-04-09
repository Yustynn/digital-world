from firebase import firebase
from os       import environ as env

URL    = env['T3_2D_DB_URL']
SECRET = env['T3_2D_DB_SECRET']
fb = firebase.FirebaseApplication(URL, SECRET)

get_temp  = lambda:   float( fb.get('/temperature') )
set_power = lambda v: fb.put('/', 'power',  v)

set_power(12)
print get_temp()

