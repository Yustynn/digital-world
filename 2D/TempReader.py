from os import system
from time import sleep

from helpers import foreach

TEMP_PATH = ''

class TempReader(object):
    def __init__(self, filepath = TEMP_PATH):
        self.filepath = filepath

        self._init_sensor()

    def next(self, interval = 0.2):
        lines = self.get_temp_lines()
        if lines[0].strip()[-3:] != 'YES':
            sleep(interval)
            return self.get_temp(interval)

        line = lines[1]
        eq_idx = line.find('t=')
        return float( line[eq_idx+1:] ) / 1000

    def _init_sensor():
        sensor_init_readings_commands = [
            'modprobe w1-gpio',
            'modprobe w1-therm'
        ]
        foreach(system, sensor_init_readings_commands)

    def _get_temp_lines():
        f = open(self.filepath, 'r')
        lines = list(f)
        f.close()
