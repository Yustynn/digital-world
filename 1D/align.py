TOLERANCE = 1.0

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def dist_to(self, p2):
        return ( (self.y-p2.y)**2 + (self.x-p2.x)**2 )**0.5
