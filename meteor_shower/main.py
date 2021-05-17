#! /Library/Frameworks/Python.framework/Versions/3.8/bin/python3.8

import sys

lnb = 0

n = 0 #number of bridgeports
m = 0 #number of bridges

edges = []
adjMat = []

# parse the input buffer and create the edge and delta lists
for line in sys.stdin:
    lst = line.split(' ')
    if lnb == 0:
        # get the graph dimensions, construct the empty adj matrix
        n = int(lst[0])
        m = int(lst[1])

        for i in range(2*n+2):          # We create a graph with 2n+2 vertices (1 per port + a source and a sink)
            adjMat.append([0]*(2*n+2))

        # connect every port to the source/sink with a vertex of capacity 2
        for i in range(n):
            adjMat[0][i+1] = 2
            adjMat[i+n+1][2*n+1] = 2

    else:
        e1 = int(lst[0])         # edge 0 is source
        e2 = int(lst[1]) + n     # edge 0 is source
        adjMat[e1][e2] = 1


    lnb = lnb + 1