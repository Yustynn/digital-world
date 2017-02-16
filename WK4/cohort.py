### PROBLEM 2 ###
compound_value_months = lambda a,i,m: round(reduce(lambda c,n: (c+a)*(1+i/12), range(m), 0),2)
print compound_value_months(200, 0.05, 8)
print compound_value_months(100, 0.05, 6)
print compound_value_months(200, 0.03, 1)

### PROBLEM 3 ###
# find_average = lambda ls: map(lambda i: [round(1.*sum(l)/len(l)) for l in ls], [0,0])
# print find_average([[2,3,4],[2,6,7],[10,5,15]])


def find_average(l2):
    list_of_avgs = [float( sum(l)/len(l) ) for l in l2]

    flattened = [float(n) for l in l2 for n in l]
    avg = round(sum(flattened) / len(flattened), 4)
    return [list_of_avgs, avg]
print find_average([[2,3,4],[2,6,7],[10,5,15]])


### PROBLEM 4 ###
transpose_matrix = lambda l: [list(m) for m in zip(*al)]

### PROBLEM 5 ###
get_details = lambda n,k,p: ([e[k] for e in p if e['name'] == n]+[None])[0]

names = ['Andrew', 'Tony', 'Jesus']
mobile_phones = [11111, 22222, 33333]
phonebook = []

for i in range(len(names)):
    phonebook.append({
        'name': names[i],
        'mobile_phone': mobile_phones[i]
    })

### PROBLEM 6 ###
get_base_counts = lambda s: ["The input DNA string is invalid", { c: s.count(c) for c in s }][all(c in "ACTG" for c in s)]

# print get_base_counts('AAB')
# print get_base_counts('AACCGT')

# print get_details('Andrew', 'mobile_phone', phonebook)
# print get_details('Andreew', 'mobile_phone', phonebook)
