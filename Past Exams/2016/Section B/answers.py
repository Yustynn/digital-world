# QUESTION 3

def norm(*zs):
    '''
    >>> norm(1+3j, 1+3j, 1-3j)
    5.477
    >>> norm(1+2j, 1+2j, 1-2j)
    3.873
    >>> norm(1+1j, 1+1j, 1-1j)
    2.449
    '''
    pass
    
    inner_sqrt = sum( map(lambda z: z*z.conjugate(), zs) )
    return round( (inner_sqrt**0.5).real, 3)

# QUESTION 4
def factors(n):
    '''
    >>> factors(6)
    [1, 2, 3, 6]
    >>> factors(12)
    [1, 2, 3, 4, 6, 12]
    >>> factors(9)
    [1, 3, 9]
    '''

    return [d for d in range(1, n+1) if not n%d]

# QUESTION 5
def combinations(start, end):
    '''
    >>> combinations(1, 7)
    ([(1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (3, 4), (3, 5), (3, 6), (3, 7), (4, 5), (4, 6), (4, 7), (5, 6), (5, 7), (6, 7)], 21)
    >>> combinations(3,5)
    ([(3, 4), (3, 5), (4, 5)], 3)
    >>> combinations(-1, 2)
    ([(-1, 0), (-1, 1), (-1, 2), (0, 1), (0, 2), (1, 2)], 6)
    >>> combinations(0,0)
    ([], 0)
    '''
    combs = []
    res = lambda: combs, len(combs)
    
    for i in range(start, end+1):
        for j in range(i+1, end+1):
            combs.append( (i, j) )

    return combs, len(combs)

if __name__ == '__main__':
    from doctest import testmod
    testmod()
