# QUESTION 1
class Coordinate(object):
    '''
    >>> p = Coordinate()
    >>> print p.x, p.y
    0 0
    >>> print p.magnitude()
    0.0
    >>> p.x = 3
    >>> p.y = 4
    >>> print p.magnitude()
    5.0
    >>> q = Coordinate(3,4)
    >>> print p == q
    True
    >>> q.translate(1, 2)
    >>> print q.x
    4
    >>> print p == q
    False
    '''
    def __init__(self, x=0, y=0):
        self.x, self.y = x, y

    def __eq__(self, p2):
        return self.x == p2.x and self.y == p2.y

    def translate(self, dx, dy):
        self.x += dx
        self.y += dy

    def magnitude(self):
        return (self.x**2 + self.y**2)**0.5

# QUESTION 2

# note: temperature is stored internally in Celsius
class Celsius(object):
    '''
    >>> c = Celsius()
    >>> c.temperature
    0
    >>> c.temperature=32
    >>> c.to_fahrenheit()
    89.6
    >>> c.temperature=-300
    >>> c.temperature
    -273
    '''
    def __init__(self, t=0):
        self._temperature = t

    def to_fahrenheit(self):
        return self.temperature * 9.0/5 + 32

    @property
    def temperature(self):
        return self._temperature

    @temperature.setter
    def temperature(self, t):
        self._temperature = max(t, -273)

    def set_temperature(self, t):
        self.temperature = t

# QUESTION 3

import time

class StopWatch(object):
    '''
    >>> sw = StopWatch()
    >>> time.sleep(0.1)
    >>> sw.stop()
    >>> print sw.elapsed_time()
    100.0
    >>> sw.start()
    >>> time.sleep(0.2)
    >>> print sw.elapsed_time()
    None
    >>> sw.stop()
    >>> print sw.elapsed_time()
    200.0
    '''

    def __init__(self):
        self.start()

    def start(self):
        self.start_time, self.end_time = time.time(), -1

    def stop(self):
        self.end_time = time.time()

    def elapsed_time(self):
        elapsed = round(self.end_time - self.start_time, 1)

        if elapsed >= 0:
            return elapsed * 1000


# QUESTION 4

class Line():
    def __init__(self, c0, c1):
        self.c0, self.c1 = map(float, (c0, c1))

    def __call__(self, x):
        return self.c0 + x*self.c1

    def table(self, start, end, n):
        stringify = lambda n: '{:>10.2f}'.format(n)

        if not n: return 'Error in printing table' #hackerman

        x = start = float(start)
        step = (end - start) / (n-1)

        res = ''
        while x <= end:
            y = self(x)

            str_x, str_y = map(stringify, [x,y])
            res += str_x + str_y + '\n'
            if not start - end: return res #hackerman2
            x += step

        return res

if __name__ == '__main__':
    from doctest import testmod
    testmod()
