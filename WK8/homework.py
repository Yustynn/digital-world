class Time(object):
    '''
    >>> t = Time(10, 19, 10)
    >>> t.elapsed_time
    37150
    >>> t.elapsed_time = 555550
    >>> print t.elapsed_time
    37150
    >>> print t
    Time: 10:19:10
    '''

    def __init__(self, h, m, s):
        self.hours, self.minutes, self.seconds = h, m, s
        self.s_per_h = 60*60
        self.s_per_m = 60

    def __str__(self):
        return 'Time: {}:{}:{}'.format(self.hours, self.minutes, self.seconds)

    @property
    def elapsed_time(self):
        s = 0
        s += self.seconds
        s += self.minutes * self.s_per_m
        s += self.hours * self.s_per_h
        return s

    @elapsed_time.setter
    def elapsed_time(self, s):
        h = s // self.s_per_h
        s -= h * self.s_per_h

        m = s // self.s_per_m
        s -= m * self.s_per_m

        h %= 24 # in case they give us more than 1 day
        self.hours, self.minutes, self.seconds = h, m, s

class Account(object):
    '''
    >>> a1 = Account('John Olsson', '19371554951', 20000)
    >>> a2 = Account('Liz Olsson', '19371564761', 20000)
    >>> a1.deposit(1000)
    >>> a1.withdraw(4000)
    >>> a2.withdraw(10500)
    >>> a1.withdraw(3500)
    >>> print a1
    John Olsson, 19371554951, balance: 13500
    >>> print a2
    Liz Olsson, 19371564761, balance: 9500
    '''
    def __init__(self, owner, account_number, amount):
        self.owner = owner
        self.account_number = account_number
        self.amount = amount

    def __str__(self):
        return '{}, {}, balance: {}'.format(self.owner, self.account_number, self.amount)

    def deposit(self, amt):
        self.amount += amt

    def withdraw(self, amt):
        self.amount -= amt

class Diff(object):
    def __init__(self, f, h=0.0001):
        self.f, self.h = f, float(h)

    def __call__(self, x):
        f, h = self.f, self.h

        return ( f(x+h) -f(x) ) / h

class Polynomial(object):
    '''
    >>> p1 = Polynomial([1, -1])
    >>> p2 = Polynomial([0, 1, 0, 0, -6, -1])
    >>> p3 = p1 + p2
    >>> print p3.coeff
    [1, 0, 0, 0, -6, -1]
    >>> p4 = p1*p2
    >>> print p4.coeff
    [0, 1, -1, 0, -6, 5, 1]
    >>> p5 = p2.derivative()
    >>> print p5.coeff
    [1, 0, 0, -24, -5]
    >>> p = Polynomial([1, 2, 3])
    >>> q = Polynomial([2, 3])
    >>> r=p-q
    >>> print r.coeff
    [-1, -1, 3]
    >>> r=q-p
    >>> print r.coeff
    [1, 1, -3]
    '''

    def __init__(self, coeff):
        self.coeff = coeff

    def __call__(self, x):
        return sum( [c*x**i for i, c in enumerate(self.coeff)] )

    def __add__(self, p2):
        c1s, c2s = self.coeff, p2.coeff
        c3s = []

        for idx in range( max(map(len, [c1s, c2s])) ):
            c = 0

            for cs in [c1s, c2s]:
                if len(cs) > idx:
                    c += cs[idx]
            c3s.append(c)

        return Polynomial(c3s)


    def __sub__(self, p2):
        c1s, c2s = self.coeff, p2.coeff
        c3s = []

        for idx in range( max(map(len, [c1s, c2s])) ):
            c = 0

            if len(c1s) > idx:
                c += c1s[idx]
            if len(c2s) > idx:
                c -= c2s[idx]
            c3s.append(c)

        return Polynomial(c3s)

    def __mul__(self, p2):
        c3s = []

        for i, c in enumerate(self.coeff):
            for j, d in enumerate(p2.coeff):
                idx = i+j
                if len(c3s) > idx:
                    c3s[idx] += c*d
                else:
                    c3s.append(c*d)

        return Polynomial(c3s)

    def _differentiate(self):
        return [c*(i+1) for i,c in enumerate(self.coeff[1:])]

    def differentiate(self):
        self.coeff = self._differentiate()

    def derivative(self):
        return Polynomial( self._differentiate() )


if __name__ == '__main__':
    import doctest
    doctest.testmod()
