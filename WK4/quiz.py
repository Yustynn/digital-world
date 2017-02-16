def printvals(num):
    ls = []
    for n in range(1, num+1):
        if n % 5 == 0 and n % 11 == 0:
            ls.append('AB')
        elif n % 5 == 0:
            ls.append('A')
        elif n % 11 == 0:
            ls.append('B')
        else:
            ls.append(n)
    return ls

print printvals(70)
