class Coordinate:
    def __init__(self, x, y):
        self.x, self.y = map(float, (x, y))

    @property
    def mag(self):
        return (self.x**2 + self.y**2)**0.5

f = open('xy.dat', 'r')

def get_maxmin_mag(f):
    coordinates = []

    for line in f:
        coordinates.append( Coordinate(*line.split()) )

    max_c = max(coordinates, key=lambda c: c.mag)
    min_c = min(coordinates, key=lambda c: c.mag)

    return (max_c.x, min_c.x)

print get_maxmin_mag(open('xy.dat', 'r'))
