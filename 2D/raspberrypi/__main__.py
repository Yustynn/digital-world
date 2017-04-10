import fb

from TempReader import TempReader
from PWM        import WaterPump

from helpers    import unblock

temp_reader = TempReader()

def update_temp():
    pump = WaterPump(32, 32)

    while 1:
        try:
            fb.set('temp', temp_reader.next_reading())
            print 'Temperature set to {}'.format(power)
        except:
            print 'Failed to set temperature in firebase'

# allows temperature to be constantly updated using a separate thread (non-blocking)
unblock(update_temp)

while 1:
    try:
        power = float( fb.get('power') )
        pump.set_power(power)
        print 'Power set to {}'.format(power)
    except:
        print 'Failed to retrieve power from firebase'
