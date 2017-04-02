from time import sleep

from Controller import Controller
from PWM        import Fan, WaterPump
from TempReader import TempReader

# find the instruments
TARGET_TEMP        = 25 # @TODO change to real temp
FAN_CHANNEL        = 18 # @TODO change to real channel
WATER_PUMP_CHANNEL = 4  # @TODO change to real channel

# assemble the orchestra
controller  = Controller(TARGET_TEMP)
fan         = Fan(FAN_CHANNEL)
temp_reader = TempReader()
water_pump  = WaterPump(WATER_PUMP_CHANNEL)

# adopt ballet pose in preparation for musical enlightenment
controller.start()

# flap arms about passionately
while 1:
   temp = temp_reader.next()
   powers = controller.step(temp)

   fan.set_power( powers.fan )
   water_pump.set_power( powers.water_pump )

   # pause to catch breath
   sleep(0.1)