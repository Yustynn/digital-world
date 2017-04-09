import RPi.GPIO as IO

IO.setwarnings(False)
IO.setmode(IO.BCM)

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

    def stop(self):
        self.pwm.stop()


class WaterPump(object):
    pwm = PWM(18)
    
    def __init__(self, pin1, pin2):
        self.channels = [Channel(pin) for pin in [pin1, pin2]]
        IO.output(self.channels[0].pin, True)
        IO.output(self.channels[1].pin, False)

    def set_power(self, power):
        self.pwm.set_power(power)

    def stop(self):
        self.pwm.stop()
