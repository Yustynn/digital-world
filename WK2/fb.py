import firebase
import json
from pprint import pprint

def print_data(res):
    data = res[1]['data']
    

    if data:
        if data['x'] and data['y']:
            print "x: {0}, y: {1}".format(data['x'], data['y'])


s = firebase.subscriber('infra-agent-126901/accelerometerData', print_data)
s.start()
