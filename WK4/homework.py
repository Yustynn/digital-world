### PROBLEM 1 ###
def get_conversion_table():
    '''
    >>> print get_conversion_table()
    [[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100], [-17.8, -12.2, -6.7, -1.1, 4.4, 10.0, 15.6, 21.1, 26.7, 32.2, 37.8], [-15.0, -10.0, -5.0, 0.0, 5.0, 10.0, 15.0, 20.0, 25.0, 30.0, 35.0]]
    '''
    f_to_c = lambda f: round( (f-32)*5/9.0, 1 )
    f_to_c_approx = lambda f: round( (f-30)/2.0, 1 )

    f_list = list( range(0, 101, 10) )
    c_list = [f_to_c(f) for f in f_list]
    c_approx_list = [f_to_c_approx(f) for f in f_list]

    return [f_list, c_list, c_approx_list]

### PROBLEM 2 ###
def max_list(l):
    return [max(l_inner) for l_inner in l]

if __name__ == '__main__':
    from doctest import testmod
    testmod()
