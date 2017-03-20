##### HELPERS #####

from functools import wraps
from copy import deepcopy as dc

# decorator to deep copy all args
def clone_args(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        return f( *dc(args), **dc(kwargs) )

    return decorator
# decorator to limit output's dp (handles tuples, lists, complex numbers and numbers)
def to_dp(n):
    def to_dp_wrapper(f):
        @wraps(f)
        def to_dp(*args, **kwargs):
            result = f(*args, **kwargs)

            if isinstance(result, complex):
                return complex( round(result.real, n), round(result.imag, n) )
            if isinstance(result, list):
                return [round(x, n) for x in result]
            if isinstance(result, tuple):
                return tuple(round(x, n) for x in result)

            return round(result, n)

        return to_dp

    return to_dp_wrapper

def ballsdeepmap(f, val):
    if isinstance(val, dict):
        return {k: ballsdeepmap(f, v) for k, v in val.iteritems()}
    elif hasattr(val, '__iter__'):
        return val.__class__( [ballsdeepmap(f, el) for el in val] )
    else:
        return f(val)

def surgery(start, fns):
    operate = lambda v, fn: fn(v)
    return reduce( operate, fns, start )









#### STARTING PROPER ####

#### QUESTION 6a #####
# f = open('sutdbook1.txt', 'r')
# lines = list(f)
# f.close()
# f = lines


# @clone_args # just in case
def get_nodes(f):
    # '''
    # >>> get_nodes(f)
    # [(0, 1), (0, 2), (0, 3), (1, 48), (1, 53)]
    # '''

    data = [tuple(line.split()) for line in list(f)]

    return ballsdeepmap(int, data)

def create_graph(nodes):
    # '''
    # >>> create_graph( get_nodes(f) )
    # {0: {1: 1, 2: 1, 3: 1}, 1: {0: 1, 48: 1, 53: 1}, 2: {0: 1}, 3: {0: 1}, 48: {1: 1}, 53: {1: 1}}
    # '''

    ids, graph = [], {}

    for node in nodes:
        for id in node:
            ids.append(id)

    ids = set(ids)

    # return other person from tuple
    other_person = lambda self, t: t[t[0] == self]

    for id in ids:
        relevant = [other_person(id, t) for t in nodes if id in t]
        graph[id] = {p2: 1 for p2 in relevant}

    return graph

def get_friends(graph, node):
    # '''
    # >>> graph = create_graph( get_nodes(f) )
    # >>> get_friends(graph, 0)
    # [1, 2, 3]
    # >>> get_friends(graph, 1)
    # [0, 48, 53]
    # >>> get_friends(graph, 2)
    # [0]
    # '''

    return graph[node].keys()

def suggested_new_friends(graph, node):
    '''
    # >>> f = list(open('facebook_less.txt', 'r'))
    # >>> g = create_graph( get_nodes(f) )
    # >>> suggested_new_friends(g, 1)
    # ([25, 88], 4)
    # >>> f = list(open('sutdbook1.txt', 'r'))
    # >>> g = create_graph( get_nodes(f) )
    # >>> suggested_new_friends(g, 0)
    # ([48, 53], 1)
    # >>> f = list(open('sutdbook2.txt', 'r'))
    # >>> g = create_graph( get_nodes(f) )
    # >>> suggested_new_friends(g, 0)
    # ([5], 3)
    '''
    curr_f = get_friends(graph, node)

    f2 = []
    for f in curr_f:
        f2 += [fr for fr in get_friends(graph, f) if fr != node]

    f2 = list(set(f2))
    num_conn = []
    for p in f2:
        num_conn.append(len( [f for f in get_friends(graph, p) if f in curr_f] ))

    max_conn = max(num_conn)

    conns = enumerate(num_conn)
    conns = [idx for idx, n in conns if n == max_conn]

    conns = [f2[i] for i in conns]
    return (conns, max_conn)


if __name__ == '__main__':
    from doctest import testmod
    testmod()
