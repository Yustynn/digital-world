class Coordinate:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def magnitude(self):
        return (self.x**2 + self.y**2)**0.5

f = open('xy.dat', 'r')

def get_maxmin_mag(f):
    coordinates = []

    for line in f:
        coordinates.append( Coordinate(*map(float,line.split())) )

    max_c = max(coordinates, key=lambda c: c.magnitude())
    min_c = min(coordinates, key=lambda c: c.magnitude())

    return (max_c.x, min_c.x)
