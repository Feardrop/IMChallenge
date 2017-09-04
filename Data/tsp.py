# nearest neighbor algorithm
#These are the steps of the algorithm:
#
#   1. Make two sets of nodes, set A and set B, and put all nodes into set B
#   2. Put your starting node into set A
#   3. Pick the node which is closest to the last node which was placed in set A and is not in set A; put this closest neighbouring node into set A
#   4. Repeat step 3 until all nodes are in set A and B is empty.

# representation of graph:
# list of nodes, at each index are a list of transitions to other nodes

def TSP (g):
    a = [0]
    b = list(range(1,len(g)))
    while b:
        # last node placed in a
        last = a[-1]
        neighbors = g[last]
        for n in neighbors:
            if n not in a:
                break
        else:
            raise(ValueError, "trapped!")
        b.remove(n)
        a.append(n)
    return a

# a b c d e
# 0 1 2 3 4
t1 = [
    [1],   # a->b
    [2],   # b->c
    [0,4], # c->a, c->e
    [1],   # d->b
    [3],   # e->d
    ]

print(TSP(t1))

# => [0, 1, 2, 4, 3]
#  a  b  c  e  d
