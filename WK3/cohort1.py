### PROBLEM 2 ###
# seriously, I'm not testing this one.
is_larger = lambda n1, n2: n1 > n2

### PROBLEM 3 ###
def letter_grade(mark):
    if (mark > 100 or mark < 0):
        return
    if (mark >= 90):
        return 'A'
    if (mark >= 80):
        return 'B'
    if (mark >= 70):
        return 'C'
    if (mark >= 60):
        return 'D'
        
    return 'E'

### PROBLEM 4 ###
def list_sum(l):
    return reduce(lambda curr_sum, next: curr_sum + next, l)

### PROBLEM 5 ###
def minmax_in_list(l):
    min, max = l[0], l[0]
    for i in xrange( len(l) ):
        n = l[i]
        if n < min:
            min = n
        if n > max:
            max = n
    return min, max

### PROBLEM 6 ###
def palindrome(n):
    '''
    >>> palindrome(15)
    False
    >>> palindrome(12321)
    True
    >>> palindrome(123212)
    False
    >>> palindrome(1)
    True
    >>> palindrome('jesus')
    False
    >>> palindrome('jesusej')
    True
    '''
    str_n = str(n)
    return str_n == str_n[::-1]

if __name__ == '__main__':
    import doctest
    doctest.testmod()
