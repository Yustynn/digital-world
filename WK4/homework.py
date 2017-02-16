### PROBLEM 1 ###
def get_conversion_table():
    '''
    >>> print get_conversion_table()
    [[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100], [-17.8, -12.2, -6.7, -1.1, 4.4, 10.0, 15.6, 21.1, 26.7, 32.2, 37.8], [-15.0, -10.0, -5.0, 0.0, 5.0, 10.0, 15.0, 20.0, 25.0, 30.0, 35.0]]
    '''
    f_to_c = lambda f: round( (f-32)*5/9.0, 1 )
    f_to_c_approx = lambda f: round( (f-30)/2.0, 1 )

    f_list = list( range(0, 101, 10) )
    c_list = map(f_to_c, f_list)
    c_approx_list = map(f_to_c_approx, f_list)

    return [f_list, c_list, c_approx_list]

### PROBLEM 2 ###

max_list=lambda l:map(max,l)
# print max_list([[100],[1,7],[-8,-2,-1],[2]])

### PROBLEM 3 ###

multiplication_table = lambda n: [[j*i for j in range(1,n+1)] for i in range(1,n+1)] or None

# print multiplication_table(7)

### PROBLEM 4 ###
# Prettier
most_frequent = lambda l: list(set( [n for n in l if l.count(n) == max( {n: l.count(n) for n in l}.values() )] ))
# Uglier
most_frequent=lambda l:list(set([n for n in l if l.count(n)==max({n: l.count(n) for n in l}.values())]))

print most_frequent([9,30,3,9,3,2,4])

### PROBLEM 5 ###
diff=lambda d:{k-1:v*k for k,v in d.items() if k}

if __name__ == '__main__':
    from doctest import testmod
    testmod()
