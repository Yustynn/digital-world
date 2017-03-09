def maxProductThree(l):
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
print maxProductThree([6,-3,-10,0,2])
print maxProductThree([6,-3,-10,0,2, 1])
print maxProductThree([6,3,-10,0,2, 1])
print maxProductThree([11, 6,-3,-10,0,2, 1])
print maxProductThree([4, 6,-3,-10,0,2, 1])
