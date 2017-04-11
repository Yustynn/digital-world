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

        metadata        = self.get_metadata(WIND_URL)
        print metadata
        self.location   = metadata['name']
        self.station_id  = metadata['device_id']

        self.temp       = self.get_temp()
        self.wind_vel   = self.get_wind_vel()

        self.update_interval = update_interval
        unblock(self.update)

    def get_metadata(self, url):
        return requests.get(url, headers=HEADERS).json()['metadata']['stations'][0]

    def get_value(self, url):
        readings = requests.get(url, headers=HEADERS).json()['items'][0]['readings']
        reading  = [reading for reading in readings if reading['station_id'] == self.station_id][0]

        return reading['value']

    def get_temp(self):
        return self.get_value(TEMP_URL) + 273.15

    def get_wind_vel(self):
        return self.get_value(WIND_URL)

    def update(self):
        while 1:
            try:
                self.temp     = self.get_temp()
                self.wind_vel = self.get_wind_vel()

                print blue( 'Temperature: {}C, Wind Velocity: {}m/s'.format(self.temp, self.wind_vel) )
            except:
                print 'Failed to retrieve temperature / wind velocity'

            sleep(self.update_interval)
