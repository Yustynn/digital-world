length = lambda x, y: (x**2 + y**2)**0.5

unfuck_python_2 = lambda f: lambda *args: f( *map(float, args) )

@unfuck_python_2
def count_lit_pixel(cx, cy, r):
    return cx, cy, r

print count_lit_pixel(1,1,1)
