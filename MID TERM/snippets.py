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
