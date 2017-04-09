from firebase import firebase
from os       import environ as env

URL    = env['T3_2D_DB_URL']
SECRET = env['T3_2D_DB_SECRET']
fb = firebase.FirebaseApplication(URL, SECRET)


make_setter = lambda k: lambda v: fb.put('/', k, v)

get_temp = lambda:   float( fb.get('/temperature') )
set_power, set_ideal_temp = map(make_setter, ['power', 'ideal_temperature'])
