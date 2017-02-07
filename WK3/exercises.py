### PROBLEM 1 ###
def may_ignore(val):
    '''
    >>> may_ignore(1)
    2
    >>> may_ignore(1.0)
    >>> may_ignore('1')
    >>> may_ignore(5)
    6
    '''
    if isinstance(val, int):
        return val + 1
    return

### PROBLEM 2 ###
def my_reverse(l):
    '''
    >>> my_reverse([5, -2, 15, 4])
    [4, 15, -2, 5]
    >>> my_reverse([4, 15, -2, 5])
    [5, -2, 15, 4]
    >>> my_reverse( my_reverse([4, 15, -2, 5]) )
    [4, 15, -2, 5]
    '''
    return l[::-1]

if __name__ == '__main__':
    from doctest import testmod
    testmod()
