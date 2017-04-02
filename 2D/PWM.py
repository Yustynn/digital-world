import RPi.GPIO as IO

IO.setwarnings(False)

# tells it to use GPIO numbers instead of PIN NUMBERs
# e.g. 19 for GPIO19 instead of 35 for PIN35 aka GPIO19
IO.setmode(IO.BCM)

IO.setup(18, IO.OUT)

class Channel(object):
    def __init__(self, pin):
        self.pin = pin

        IO.setup(pin, IO.OUT)
        self.pwm = IO.PWM(pin, 50)

class PWM(Channel):
    def __init__(self, pin):
        super(PWM, self).__init__(pin)
        self.pwm.start(0)

    def set_power(self, power):
        self.pwm.ChangeDutyCycle(power * 100)
        print 'power set to '+str(power)

p = PWM(18)
p.start(0)

class WaterPump(object):
    def __init__(self, pin1, pin2):
        self.channels = [Channel(pin) for pin in [pin1, pin2]]
        IO.output(self.channels[0].pin, True)
        IO.output(self.channels[1].pin, False)

    def set_power(self, power):
        p.set_power(power)
