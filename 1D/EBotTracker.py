from math   import acos, pi
from utils  import Point, Line

class EBotTracker(object):
    '''
    >>> from math import pi
    >>> coords = [ [0,0], [1,1], [1,-1], [-1,-1], [-1,1] ]
    >>> points = map(lambda c: Point(*c), coords)
    >>> theta = pi/8
    >>> e = EBotTracker(points[0], points[1])
    >>> e.orientation
    True
    >>> e = EBotTracker(points[0], points[2])
    >>> e.orientation == theta + pi/4
    True
    >>> e = EBotTracker(points[0], points[3])
    >>> e.orientation == theta + 2*pi/4
    True
    >>> e = EBotTracker(points[0], points[4])
    >>> e.orientation == theta + 3*pi/4
    True
    '''
    def __init__(self, front=Point(0,0), back=Point(0,0)):
        self.front = front
        self.back  = back

    @property
    def orientation(self):
        front, back = self.front, self.back

        c3  = Point(front.y, back.x) # for getting theta
        hyp = front.dist(back) or 1E-10
        adj = front.dist(c3)

        theta = acos((adj / hyp)%1)

        is_front_x_gte = front.x >= back.x
        is_front_y_gte = front.y >= back.y

        if is_front_x_gte and is_front_y_gte:
            quad = 1
        elif is_front_y_gte:
            quad = 4
        elif is_front_x_gte:
            quad = 2
        else:
            quad = 3

        theta += (quad-1) * (pi/4)

        return theta

if __name__ == '__main__':
    import doctest
    doctest.testmod()
