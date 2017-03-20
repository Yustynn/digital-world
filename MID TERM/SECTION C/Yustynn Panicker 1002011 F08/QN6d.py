def suggested_new_friends(graph, node):
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
