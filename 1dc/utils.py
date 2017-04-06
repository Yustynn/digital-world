from math import acos, pi

# so I went a little overboard with magic methods for no good reason at all
class Point(object):
    '''
    >>> a = Point([0,0])
    >>> b = Point([0,5])
    >>> c = Point([1,5])
    >>> a.x
    0.0
    >>> b.y
    5.0
    >>> a.dist(b)
    5.0
    >>> a.grad(b)
    50000000000.0
    >>> a.grad(c)
    5.0
    '''

    def __init__(self, coords): # coords can be np
        self.x, self.y = map(float, list(coords))

    def __add__(c1, c2):
        return Point([c1.x + c2.x, c1.y + c2.y ])

    def __neg__(self):
        return Point([-self.x, -self.y])

    def __sub__(c1, c2):
        return Point([c1.x - c2.x, c1.y - c2.y ])

    def __str__(self):
        return 'x: {:2f}, y: {:2f}'.format(self.x, self.y)

    def grad(c1, c2):
        d_x = c2.x - c1.x
        d_y = c2.y - c1.y

        if not d_x:
            d_x = 1E-10

        return d_y / d_x

    def dist(c1, c2):
        return ((c2.x - c1.x)**2 + (c2.y - c1.y)**2)**0.5

class EBotTracker(object):
    '''
    >>> from math import pi
    >>> coords = [ [0,0], [1,1], [1,-1], [-1,-1], [-1,1] ]
    >>> points = map(Point, coords)
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
    def __init__(self, front=Point([0,0]), back=Point([0,0])):
        self.front = front
        self.back  = back

    @property
    def orientation(self):
        front, back = self.front, self.back

        c3  = Point([front.y, back.x]) # for getting theta
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
