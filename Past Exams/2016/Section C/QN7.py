def maxProductThree(l):
    '''
    TEST CASE 1:   0 positive numbers
    >>> maxProductThree([-5, -10, -12, -7])
    -350
    
    TEST CASE 2:   1 positive number
    >>> maxProductThree([-5, 10, -12, -7])
    840
    
    TEST CASE 3:   2 positive numbers
    >>> maxProductThree([-5, 10, -12, 7])
    600
    
    TEST CASE 4a: >3 positive numbers
    >>> maxProductThree([-5, 10, 1, -12, 7])
    600
    
    TEST CASE 4b: >3 positive numbers
    >>> maxProductThree([-5, 10, 9, -12, 7])
    630
    '''
    prod = lambda nums: reduce(lambda prev, curr: prev*curr, nums)
    l.sort()
    positive = [n for n in l if n > 0]
    negative = [n for n in l if n < 0]

    num_positive = len(positive)

    if num_positive == 0:
        return prod(l[-3:])
    if num_positive == 1:
        return prod(l[0:2] + [l[-1]])
    if num_positive == 2:
        return prod(positive[-1:] + negative[-2:])

    neg_poss = prod(negative[0:2])
    pos_poss = prod(positive[-3:-1])

    return l[-1] * max(neg_poss, pos_poss)

# Test Cases
#print maxProductThree([6,-3,-10,0,2])
#print maxProductThree([6,-3,-10,0,2, 1])
#print maxProductThree([6,3,-10,0,2, 1])
#print maxProductThree([11, 6,-3,-10,0,2, 1])
#print maxProductThree([4, 6,-3,-10,0,2, 1])

if __name__ == '__main__':
    import doctest
    doctest.testmod()
