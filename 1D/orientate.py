class Line(object):
    def __init__(self, p1, p2):
        self.grad = (p2.y - p1.y) / (p2.x - p1.x)
        self.c    = p2.y - self.grad*p2.x
        self.ref  = (p1 + p2)/2

    def __call__(self, x):
        return self.grad*x + self.c

    def contains(self, p, tolerance=5):
        tolerance *= abs(self.ref.x - p.x)
        
        return abs( self(p.x) - p.y ) < tolerance

