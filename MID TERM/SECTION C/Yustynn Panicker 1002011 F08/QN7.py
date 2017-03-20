
### STARTING PROPER ###
def num_of_sol(n):

    def further(n):
        res = []
        for num in range(n):
            res.append([num, n - num])

        res = [sorted(ls) for ls in res]
        return res

    print further(5)

    # sols = []
    #
    # for i in range(0, ans+1):
    #     sol = []
    #     curr = i
    #     while len(sol) < 5 and curr < n:
    #         for (n in curr):
    #             rem = n - curr
    #
    #             if sum(sol) > n:
    #                 break
    #
    #     if sum(sol) == n:
    #         sols.append(sol)
    #     x2 = n - x1

    # for x1 in range(1, ans+1):
    #     curr = x1


    # based on unique values, count num soln
    count = 0
    sols = [ [3], [1,2], [1,1,1] ]
    for sol in sols:
        count += 5**(len(set(sol))-1)

    return count

print num_of_sol(3)
