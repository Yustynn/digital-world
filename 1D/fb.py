from firebase   import firebase
from threading  import Thread

# firebase setup
URL = "https://dw-1d-ebot.firebaseio.com/"
TOKEN = "avxnAEHlshI3X9XUYWpa88AgOsbBmx30DdSV6hqN"

fb = firebase.FirebaseApplication(URL, TOKEN)

def update(points):
    def updater():
        # FIREBASE UPDATE
        print 'Updating firebase...'
        try:
            for key, point in points.iteritems():
                fb.put('/', key, point)
            print 'Firebase updated!'
        except:
            print 'Firebase update failed'

    t = Thread(target=updater)
    t.daemon = True
    t.start()
