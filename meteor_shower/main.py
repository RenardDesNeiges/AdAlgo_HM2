#! /Library/Frameworks/Python.framework/Versions/3.8/bin/python3.8

import sys
import math
import random

# works by reference, do not deepcopy before calling
def contract(E,ec,V):
    v1 = ec[0]
    v2 = ec[1]
    # contraction procedure over edgelist
    for i in range(len(E) - 1, -1, -1):
        e = E[i]
        if e == ec or e == [v2,v1]:
            del E[i]
            continue
        if e[0] == v2:
            e[0] = v1
        if e[1] == v2:
            e[1] = v1
    # remove the second vertex from the vertices list
    V.remove(v2)

# note, deepcopy the graph before calling the function because it will modify the original datastructures
def modKargStein(E,V,n,alpha,C):
    if n == 3 : 
        # pick cut uniformly at random in V choose 2
        pass
    else:
        for i in range(1, n- math.ceil(math.pow(2, 1/(2+2*alpha) ) ) ):
            # choose e uniformly at random in E, contract E by e

            ec = E[random.randrange(len(E))]    # uniformly random edge
            contract(E,ec,V)
            pass
        # Call ModKargStein twice on the output of the procedure so far, return the critical sets that are C or C+1
"""
    Parsing the input 
"""

lnb = 0

n = 0 # number of vertices
m = 0 # number of edges

E = []
V = []

# parse the input buffer and create the edge and delta lists
for line in sys.stdin:
    lst = line.split(' ')
    if lnb == 0:
        # get the graph dimensions, construct the empty adj matrix
        n = int(lst[0])
        m = int(lst[1])

        # we create the vertices list
        for i in range(1,n+1):
            V.append(i)

    else:
        e1 = int(lst[0])
        e2 = int(lst[1])
        E.append([e1,e2])

    lnb = lnb + 1

print(V)

contract(E,[1,2],V)
print(V)