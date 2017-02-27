def second_item_list(l2): return [l1[1] if len(l1) > 1 else None for l1 in l2]

print second_item_list([[100],[1,7],[8,0,-1],[2]])

from time import sleep

def wait(): return sleep(0.5)

# memoization
def optimize_is_triangle(f):
    cache = {}
    def wrapper(*args):
        n = args[0]
        if n not in cache.keys():
            res = f(*args)
            print 'res', n, res, args
            cache[n] = res
        # print cache
        return cache[n]
    return wrapper

@optimize_is_triangle
def is_triangle(n, lvl=1):
    return n == 0 if n < 1 else is_triangle(n-lvl, lvl+1)

for n in [1,2,5,6]:
    print n, is_triangle(n)
    wait()

#
# def is_triangle(n):
#     lvl = 1
#     while True:
#         if n > 0:
#             n -= lvl
#             lvl += 1
#         else:
#             return n == 0
