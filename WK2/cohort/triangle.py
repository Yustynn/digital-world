from math import sqrt

class Coordinate:
    x = 0
    y = 0

def area_of_triangle(*points):
  def get_len(p1, p2):
      return sqrt( (p1.x-p2.x)**2 + (p1.y-p2.y)**2 )

  side_lens = []
  for i in xrange(0, 3):
    p1 = points[i]
    p2 = points[ (i+1) % 3 ]
    side_lens.append( get_len(p1, p2) )

  s = sum(side_lens) / 2

  side_lens = side_lens[::-1]

  ans = sqrt( reduce(lambda curr,l: curr*(s-l), side_lens, s ) )
  return round(ans, 2)

points = []

for pt_num in ['first', 'second', 'third']:
    p = Coordinate()

    p.x = float( raw_input("Enter x coordinate of the {0} point of a triangle: ".format(pt_num)) )
    p.y = float( raw_input("Enter y coordinate of the {0} point of a triangle: ".format(pt_num)) )

    points.append(p)

print "\033[92mThe area of the triangle is {0}".format( area_of_triangle(*points) )
