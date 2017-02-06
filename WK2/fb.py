import firebase
import json
from pprint import pprint
from eBot import eBot

MAX_VAL = 10.0


# ebot = eBot.eBot() # create an eBot object
# ebot.connect() # connect to the eBot via Bluetooth


def normalize(s):
    if s > 0:
        return min([s / MAX_VAL, 1])
    else:
        return max([s / MAX_VAL, -1])

def print_data(res):
    data = res[1]['data']
    try:
        # print "x: {0}, y: {1}".format(data['x'], data['y'])
        coord_vals = map(lambda c: data[c], ['y', 'x'])
        forward_val = coord_vals[0]
        turn_val = coord_vals[1]
        speed1 = forward_val
        speed2 = forward_val

        speed1 += turn_val
        speed2 -= turn_val

        speeds = map(normalize, [speed1, speed2])

        print "x: {0},y: {1}".format(coord_vals[0], coord_vals[1])
        print "S1: {0}, S2: {1}".format(speeds[0], speeds[1])

  #      ebot.wheels(*speeds)
    except:
   #     ebot.wheels(0,0)
        print 'badness'


s = firebase.subscriber('infra-agent-126901', print_data)
s.start()
