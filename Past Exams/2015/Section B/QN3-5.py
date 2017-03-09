# The things in ''' are test cases.
# If they pass, nothing will happen.
# If they fail, Python will tell you.


############### QUESTION 3 ###############
def comp(x):
    '''
    >>> comp(2)
    37
    >>> comp(3)
    82
    '''

    return x**3 + 4*x**2 + 6*x + 1

############### QUESTION 4 ###############

def genList(start, end):
    '''
    >>> genList(2,12)
    [3, 6, 9, 12]
    >>> genList(2,20)
    [3, 6, 9, 12, 15, 18]
    '''
    result = []

    for n in range(start, end+1):
        if n % 3 == 0:
            result.append(n)

    return result

# More advanced version
def genList(start, end, divisor=3):
    '''
    >>> genList(2,12)
    [3, 6, 9, 12]
    >>> genList(2,20)
    [3, 6, 9, 12, 15, 18]
    '''

    return [n for n in range(start, end+1) if not n % divisor]

############### QUESTION 5 ###############

def matAdd(A, B):
    '''
    >>> A = [[1,2,3], [4, 5, 6]]
    >>> B = [[10,20,30], [40, 50, 60]]
    >>> C = matAdd(A,B)
    >>> C
    [[11, 22, 33], [44, 55, 66]]
    '''

    C = []

    for y in range( len(A) ):
        column = []
        for x in range( len(A[0]) ):
            column.append( A[y][x] + B[y][x] )
        C.append(column)

    return C

if __name__ == '__main__':
    from doctest import testmod
    testmod()
