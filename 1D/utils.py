from math import acos, pi

TEST_LOG = True

def tlog(*args):
    if TEST_LOG:
        for arg in args:
            print arg

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

    def __add__(c1, c2):
        return Point(c1.x + c2.x, c1.y + c2.y )

    def __eq__(p1, p2):
        return p1.x == p2.x and p1.y == p2.y

    def __neg__(self):
        return Point(-self.x, -self.y)

    def __sub__(c1, c2):
        return Point(c1.x - c2.x, c1.y - c2.y)

    def __str__(self):
        return 'x: {:>5.1f}, y: {:>5.1f}'.format(self.x, self.y)

    def grad(c1, c2):
        d_x = c2.x - c1.x
        d_y = c2.y - c1.y

        if not d_x:
            d_x = 1E-10

        return d_y / d_x

    def dist_to(c1, c2):
        return ((c2.x - c1.x)**2 + (c2.y - c1.y)**2)**0.5

    @property
    def exists(self):
        return self.x != 256 and self.y != 192

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
        # tlog('Actual Y: {:>5.1f}, Expected Y: {:>5.1f}, Diff: {:>5.1f}, Tol: {:.1f}'.format(p.y, self(p.x), abs( self(p.x) - p.y ), tolerance))
#
        closest = self.closest_point_to(p)
        print 'Actual: {}, Closest: {}, Distance: {:>5.1f}'.format(p, closest, closest.dist_to(p))
        print self
        return closest.dist_to(p) < tolerance
        # return abs( self(p.x) - p.y ) < tolerance

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
