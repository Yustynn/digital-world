from math import acos, pi

from constants import CAMERA_X_MAX, CAMERA_Y_MAX
from helpers   import log, tlog

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
    >>> a.dist_to(b)
    5.0
    >>> a.grad(b)
    50000000000.0
    >>> a.grad(c)
    5.0
    '''

    def __init__(self, x=0, y=0): # coords can be np
        self.x, self.y = map(float, [x,y])

    def __add__(p1, p2):
        return Point(p1.x + p2.x, p1.y + p2.y )

    def __eq__(p1, p2):
        return p1.x == p2.x and p1.y == p2.y

    def __neg__(self):
        return Point(-self.x, -self.y)

    def __sub__(p1, p2):
        return Point(p1.x - p2.x, p1.y - p2.y)

    def __str__(self):
        return 'x: {:>5.1f}, y: {:>5.1f}'.format(self.x, self.y)

    def dist_to(p1, p2):
        return ((p2.x - p1.x)**2 + (p2.y - p1.y)**2)**0.5

    def grad(p1, p2):
        d_x = p2.x - p1.x
        d_y = p2.y - p1.y

        if not d_x:
            d_x = 1E-10

        return d_y / d_x

    @property
    def exists(self):
        return self.x != CAMERA_X_MAX/2 and self.y != CAMERA_Y_MAX/2

    # Vector method
    @property
    def mag(self):
        return self.dist_to(Point(0,0))


class Line(object):
    '''
    >>> l = Line(2.5, 10)
    >>> l(10)
    35.0
    >>> l.contains(Point(1,1))
    False
    >>> l.contains(Point(100, 260))
    True
    >>> p = l.intersect_with(Line(7,3))
    >>> print p
    x:   1.6, y:  13.9
    '''
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

    def __str__(self):
        return 'y = {:.2f}x + {:.2f}'.format(self.m, self.c)

    # @TODO make tolerance a function of distance
    def contains(self, p, tolerance=25):
        closest = self.closest_point_to(p)
        tlog( 'Actual: {}, Closest: {}, Distance: {:>5.1f}'.format(p, closest, closest.dist_to(p)) )

        return closest.dist_to(p) < tolerance

    def closest_point_to(self, p):
        m2 = -1/ (self.m or 1E-10)
        c2 = p.y - m2*p.x

        closest_tangent = Line(m2, c2)
        return self.intersect_with(closest_tangent)

    def intersect_with(line1, line2):
        m1, c1 = line1.m, line1.c
        m2, c2 = line2.m, line2.c

        x = (c2 - c1) / (m1 - m2)
        y = line1(x)

        return Point(x, y)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
