import firebase
import json
from pprint import pprint

def print_data(res):
    data = res[1]['data']
    print type(data)
    
    pprint(data)
    
    if data:
        print "x: {0}, y: {1}".format(data['x'], data['y'])


s = firebase.subscriber('infra-agent-126901', print_data)
s.start()
