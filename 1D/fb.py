from firebase   import firebase
from threading  import Thread

from helpers    import log, tlog

# firebase setup
URL = "https://dw-1d-ebot.firebaseio.com/"
TOKEN = "avxnAEHlshI3X9XUYWpa88AgOsbBmx30DdSV6hqN"

fb = firebase.FirebaseApplication(URL, TOKEN)

def update_points(points):
    def updater():
        # FIREBASE UPDATE
        log( 'Updating firebase...', color='blue' )
        try:
            for key, point in points.iteritems():
                fb.put('/', key, point)
            log( 'Firebase updated!', color='blue' )
        except:
            log( 'Firebase update failed', color='red' )

    t = Thread(target=updater)
    t.daemon = True
    t.start()
