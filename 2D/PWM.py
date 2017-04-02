import RPi.GPIO as IO

IO.setwarnings(False)

# tells it to use GPIO numbers instead of PIN NUMBERs
# e.g. 19 for GPIO19 instead of 35 for PIN35 aka GPIO19
IO.setmode(IO.BCM) 


class PWM(object):
    def __init__(self, channel):
        io.setup(channel, IO.OUT)
        self.pwm = IO.PWM(channel, 100)
        self.pwm.start(0)

    def set_power(self, power):
        self.ChangeDutyCycle(power*100)

class WaterPump(PWM):
    def __init__(self, channel):
        super(WaterPump, self).__init__(channel)

class Fan(PWM):
    def __init__(self, channel):
        super(WaterPump, self).__init__(channel)
