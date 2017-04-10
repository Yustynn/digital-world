import requests

from os         import environ
from time       import sleep

from helpers    import blue, unblock

API_KEY  = environ['DATA_GOV_API_KEY']
WIND_URL = 'https://api.data.gov.sg/v1/environment/wind-speed'
TEMP_URL = 'https://api.data.gov.sg/v1/environment/air-temperature'

HEADERS = {'Content-Type': 'application/json', 'api-key': API_KEY}

class EnvConditions(object):
    def __init__(self, update_interval = 60):
        self.temp     = self.get_temp()
        self.wind_vel = self.get_wind_vel()
        
        self.update_interval = update_interval
        unblock(self.update)

    def get_and_parse(self, url):
        return requests.get(url, headers=HEADERS).json()['items'][0]['readings'][0]['value']

    def get_temp(self):
        return self.get_and_parse(TEMP_URL) + 273.15

    def get_wind_vel(self):
        return self.get_and_parse(WIND_URL)

    def update(self):
        while 1:
            try:
                print 'hi'
                self.temp     = self.get_temp()
                self.wind_vel = self.get_wind_vel()

                print 'huh'
                print blue( 'Temperature: {}C, Wind Velocity: {}m/s'.format(self.temp, self.wind_vel) ) 
            except:
                print 'Failed to retrieve temperature / wind velocity'

            sleep(self.update_interval)
