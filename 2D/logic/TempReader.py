from glob import glob
from os   import system
from time import sleep

from helpers import foreach

base_dir = '/sys/bus/w1/devices/'
device_folder = glob(base_dir + '28*')[0]
TEMP_PATH = device_folder + '/w1_slave'

class TempReader(object):
    def __init__(self, filepath = TEMP_PATH):
        self.filepath = filepath

        self._init_sensor()

    def next_reading(self, interval = 0.2):
        lines = self._get_temp_lines()

        if lines[0].strip()[-3:] != 'YES':
            sleep(interval)
            return self.get_temp(interval)

        line = lines[1]
        eq_idx = line.find('t=')
        return float( line[eq_idx+2:] ) / 1000

    def _init_sensor(self):
        sensor_init_readings_commands = [
            'modprobe w1-gpio',
            'modprobe w1-therm'
        ]
        foreach(system, sensor_init_readings_commands)

    def _get_temp_lines(self):
        f = open(self.filepath, 'r')
        lines = list(f)
        f.close()

        return lines
