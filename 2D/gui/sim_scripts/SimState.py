import requests

from os         import environ
from time       import sleep

from helpers    import unblock, yellow_bold

API_KEY  = environ['DATA_GOV_API_KEY']
WIND_URL = 'https://api.data.gov.sg/v1/environment/wind-speed'
TEMP_URL = 'https://api.data.gov.sg/v1/environment/air-temperature'
UV_URL   = 'https://api.data.gov.sg/v1/environment/uv-index'

HEADERS = {'Content-Type': 'application/json', 'api-key': API_KEY}

class SimState(object):
    def __init__(self, update_interval = 60):
        self.power          = 0.0 # [0.0:1.0]
        self.power_consumed = 0.0 # (J)

        metadata         = self.get_metadata(WIND_URL)
        self.location    = metadata['name']
        self.station_id  = metadata['device_id']

        self.temp             = self.get_temp()
        self.wind_vel         = self.get_wind_vel()
        self.solar_irradiance = self.get_solar_irradiance()

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

    def get_solar_irradiance(self):
        uv_idx = requests.get(UV_URL, headers=HEADERS).json()['items'][0]['index'][0]['value']

        # approx uv -> solar irrad. equation from http://www.weather-watch.com/smf/index.php?topic=30060.0
        return uv_idx * 100

    def update(self):
        count = 0
        while 1:
            try:
                self.temp     = self.get_temp()
                self.wind_vel = self.get_wind_vel()

                count += 1

                if count > 5:
                    self.solar_irradiance = self.get_solar_irradiance()
                    count = 0

                print yellow_bold( 'Temperature: {}C, Wind Velocity: {}m/s'.format(self.temp-273.15, self.wind_vel) )
            except:
                print 'Failed to retrieve temperature / wind velocity'

            sleep(self.update_interval)
