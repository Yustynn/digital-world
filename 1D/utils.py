from math import acos, pi

# so I went a little overboard with magic methods for no good reason at all
class Point(object):
    '''
    >>> a = Point(0,0)
    >>> b = Point(0,5)
    >>> c = Point(1,5)
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

    def __init__(self, x=0, y=0): # coords can be np
        self.x, self.y = map(float, [x,y])

    def __add__(c1, c2):
        return Point(c1.x + c2.x, c1.y + c2.y )

    def __neg__(self):
        return Point(-self.x, -self.y)

    def __sub__(c1, c2):
        return Point(c1.x - c2.x, c1.y - c2.y)

    def __str__(self):
        return 'x: {:2f}, y: {:2f}'.format(self.x, self.y)

    def grad(c1, c2):
        d_x = c2.x - c1.x
        d_y = c2.y - c1.y

        if not d_x:
            d_x = 1E-10

        return d_y / d_x

    def dist_to(c1, c2):
        return ((c2.x - c1.x)**2 + (c2.y - c1.y)**2)**0.5

    # Vector method
    @property
    def mag(self):
        return self.dist_to(Point(0,0))

class Line(object):
    @staticmethod
    def from_points(p1, p2):
        m = (p2.y - p1.y) / ( (p2.x - p1.x) or 1E-10)
        c = p1.y - m*p1.x
        return Line(m, c)

    def __init__(self, m, c):
        self.m = m
        self.c = c

    def __call__(self, x):
        return self.m*x + self.c

    # @TODO make tolerance a function of distance
    def contains(self, p, tolerance=5):
        return abs( self(p.x) - p.y ) < tolerance

    def closest_point_to(self, p):
        m2 = -1/self.m
        c2 = p.y - m2*p.x

        tangent = Line(m2, c2)

        return self.intersect_with(tangent)

    def intersect_with(line1, line2):
        m1, c1 = line1.m, line1.c
        m2, c2 = line2.m, line2.c

        x = (c2 - c1) / (m1 - m2)
        y = line1(x)

        return Point(x, y)
