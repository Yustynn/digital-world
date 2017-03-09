# let's be real, who gives a fuck about cx and cy?

def countLitPixel(cx, cy, r):
    # Below in the ''' comments are test cases that run automatically.
    # If they fail, it'll tell you. If they pass, it won't tell you.
    '''
    >>> countLitPixel(5, 2, 5)
    88
    >>> countLitPixel(1, 1, 1)
    4
    '''

    count = 0
    # below is a one-line function w/ args `x` and `y`. RHS of `:` gets returned
    is_lt_r = lambda x, y: r > (x**2 + y**2)**0.5

    for x in range(-r, r+1):
        for y in range(-r, r+1):
            lbcorner = [x,   y  ]
            rbcorner = [x+1, y  ]
            ltcorner = [x,   y+1]
            rtcorner = [x+1, y+1]

            corners = [ ltcorner, rtcorner,
                        lbcorner, rbcorner ]

            # `any` returns True if there are any elements in an iterable (e.g a List)
            # that are truthy
            #
            # This uses a list comprehension, and abuses the fact that True == 1
            # and False == 0 in Python.
            #
            # If you're uncomfortable with this, it's fine. The logic is just to
            # check if any corners' coordinates are < radius. If any are, add 1
            # to the count. Just do it the longer way
            count += any( [is_lt_r(*coords) for coords in corners] )
    return count

if __name__ == '__main__':
    from doctest import testmod
    testmod()
