
# PART A
# bad naming, should follow snake case convention (python is a snake)
def readMatrix(f):
    '''
    >>> readMatrix( open('gauss2.txt', 'r') )
    {'matrix': [[2.0, -1.0, 0.0, 1.0, 0.0, 0.0], [-1.0, 2.0, -1.0, 0.0, 1.0, 0.0], [0.0, -1.0, 2.0, 0.0, 0.0, 1.0]], 'op': [['2', '0', '0.5', '1'], ['1', '1', '0.666666666667'], ['2', '1', '1', '2'], ['1', '2', '0.75'], ['2', '2', '0.666666666667', '1'], ['2', '1', '1', '0'], ['1', '0', '0.5']]}
    '''
    
    res = { 'matrix': [], 'op': [] }

    is_matrix = True
    curr = res['matrix']

    for line in list(f)[1:-1]:
        data = line.split()

        if len(data) == 1:
            is_matrix = False
            curr = res['op']
        else:

            if is_matrix:
                data = map(float, data)
            curr.append(data)
    return res

# PART B
from copy import deepcopy as dc
from functools import wraps

def clone_args(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        return f( *dc(args), **dc(kwargs) )

    return decorator

@clone_args
def mulRowByC(m, i, c):
    '''
    >>> A=[[0,2,1,-1],[0,0,3,1],[0,0,0,0]]
    >>> mulRowByC(A,0,2)
    [[0, 4, 2, -2], [0, 0, 3, 1], [0, 0, 0, 0]]
    '''
    m[i] = [n*c for n in m[i]]

    return m

@clone_args
def addRowMulByC(m, i, c, j):
    '''
    >>> A=[[0,2,1,-1],[0,0,3,1],[0,0,0,0]]
    >>> addRowMulByC(A,0,0.5,1)
    [[0, 2, 1, -1], [0.0, 1.0, 3.5, 0.5], [0, 0, 0, 0]]
    '''
    
    m[j] = [nj + c*ni for ni, nj in zip(m[i], m[j])]

    return m

@clone_args
def gaussElimination(data):
    '''
    >>> data = {'matrix': [[2.0, -1.0, 0.0, 1.0, 0.0, 0.0], [-1.0, 2.0, -1.0, 0.0, 1.0, 0.0], [0.0, -1.0, 2.0, 0.0, 0.0, 1.0]], 'op': [['2','0', '0.5', '1'], ['1', '1', '0.666666666667'], ['2', '1', '1', '2'], ['1', '2', '0.75'], ['2', '2', '0.666666666667', '1'], ['2', '1', '1', '0'], ['1', '0', '0.5']]}
    >>> matA, result = gaussElimination(data)
    >>> print matA
    [[2.0, -1.0, 0.0, 1.0, 0.0, 0.0], [-1.0, 2.0, -1.0, 0.0, 1.0, 0.0], [0.0, -1.0, 2.0, 0.0, 0.0, 1.0]]
    >>> print result
    [[1.0, 0.0, -0.0, 0.75, 0.5, 0.25], [0.0, 1.0, -0.0, 0.5, 1.0, 0.5], [0.0, 0.0, 1.0, 0.25, 0.5, 0.75]]
    '''
    op_to_fn = {
        '1': mulRowByC,
        '2': addRowMulByC
    }

    orig = res = data['matrix']

    for l in data['op']:
        fn = op_to_fn[l.pop(0)]
        args = [res, int(l[0]), float(l[1])] 
        if len(l) == 3: args.append( int(l[2]) )

        res = fn(*args)

    res = [[round(n, 2) for n in row] for row in res]

    return orig, res

if __name__ == '__main__':
    import doctest
    doctest.testmod()
