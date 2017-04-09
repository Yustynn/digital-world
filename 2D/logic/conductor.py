from time import sleep, strftime

from Controller import Controller
from PWM        import WaterPump
from TempReader import TempReader

# find the instruments
TARGET_TEMP         = 28.5
WATER_PUMP_CHANNEL1 = 16
WATER_PUMP_CHANNEL2 = 20

# assemble the orchestra
controller  = Controller(TARGET_TEMP)
temp_reader = TempReader()
water_pump  = WaterPump(WATER_PUMP_CHANNEL1, WATER_PUMP_CHANNEL2)

# adopt ballet pose in preparation for musical enlightenment
controller.start()

# flap arms about passionately
try:
    while 1:
       temp = temp_reader.next_reading()
       powers = controller.step(temp)

       print 'Temperature {:.3f} at {}'.format(temp,  strftime('%H:%M:%S'))

       water_pump.set_power( powers.water_pump )

       # pause to catch breath
       sleep(0.1)

# the performance ends
except KeyboardInterrupt:
    water_pump.stop()
