#! /Library/Frameworks/Python.framework/Versions/3.8/bin/python3.8

import sys
import math
import random
import copy
import time

# contracts an edge according to Karger's algorithm's edge contraction procedure
# works by reference, do not deepcopy before calling
def contract(E,ec,V):
    v1 = ec[0]
    v2 = ec[1]
    # contraction procedure over edgelist (we iterate backwards over the list so deletion is seemless)
    for i in range(len(E) - 1, -1, -1):
        e = E[i]
        if (e[0] == v1 and e[1] == v2) or (e[1] == v1 and e[0] == v2) :
            del E[i]
            continue
        if e[0] == v2:
            e[0] = v1
        if e[1] == v2:
            e[1] = v1
    # remove the second vertex from the vertices list
    V.remove(v2)

# modified Karger-Stein algorithm
# note, deepcopy the graph before calling the function because it will modify the original datastructures
def modKargStein(E,V,n,alpha):
    if n == 3 : 
        # pick cut uniformly at random in V choose 2
        i = random.randrange(3)
        j = (i + random.randrange(1,3))%3
        ec = [V[i], V[j]]   #critical edge uniformly picked at random among possible cuts
        contract(E,ec,V)    # contract the graph

    else:
        for i in range(1, n- math.ceil(math.pow(2, 1/(2+2*alpha) ) ) ):
            # choose e uniformly at random in E, contract E by e
            ec = E[random.randrange(len(E))]    # choose an edge uniformly at random 
            contract(E,ec,V)                    # contract it in G
        
        # Call ModKargStein twice on the output of the procedure so far
        E1 = copy.deepcopy(E)
        V1 = copy.deepcopy(V)
        modKargStein(E1, V1, len(V1), alpha)
        E2 = copy.deepcopy(E)
        V2 = copy.deepcopy(V)
        modKargStein(E2, V2, len(V2), alpha)

        # return the critical sets 
        return E1, E2 #min(len(E1),len(E2))
        

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
        # edge reprensentaiton is a bit shady : we use ((v1,v2,v1,v2)) where the first tuple will be affected by contraction but not the second (which allows to keep track of cuts that are obtained)
        E.append([e1,e2,e1,e2])

    lnb = lnb + 1

C = m

O = 1
start = time.time()

critsets = []

## find a min-cut 
# for i in range(O * math.ceil(math.pow(n,3)*math.log(n))):
while time.time() - start < 3.8:
    Ei = copy.deepcopy(E)
    Vi = copy.deepcopy(V)
    E1, E2 = modKargStein(Ei,Vi,n,1)
    nmc = min(len(E1),len(E2))

    C1 = frozenset([frozenset([el[2],el[3]]) for el in E1])
    C2 = frozenset([frozenset([el[2],el[3]]) for el in E2])

    if len(C1) <= (C + 1):
        if C1 not in critsets:
            critsets.append(C1)
    if len(C2) <= (C + 1):
        if C2 not in critsets:
            critsets.append(C2)

    # if we reduce the size of the cut we need to clean our set of critical sets
    if nmc < C:
        C = nmc
        for i in range(len(critsets) - 1, -1, -1):
            Es = critsets[i]
            if len(Es) > C+1:
                del critsets[i]

print(C)
# print([len(el) for el in critsets])
for i in range(len(critsets) - 1, -1, -1):
            Es = critsets[i]
            if len(Es) == C:
                del critsets[i]
print(len(critsets))