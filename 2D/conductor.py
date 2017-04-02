from time import sleep

from Controller import Controller
from PWM        import Fan, WaterPump
from TempReader import TempReader

# assemble the orchestra
controller  = Controller()
fan         = Fan(0)
temp_reader = TempReader()
water_pump  = WaterPump(0)

# flap arms about passionately
while 1:
   temp = temp_reader.next()
   powers = controller.step(temp)

   fan.set_power( powers.fan )
   water_pump.set_power( powers.water_pump )
   
   # exhausted from the hard work
   sleep(0.1)
