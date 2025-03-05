from typing import List

def ring_graph(NQ):
    g = []
    if NQ == 2:
        return [[0,1]]
    else:
        for i in range(NQ):
            if i % 2 == 0 and i +1 != NQ:
                g.append([i,i+1])
        if NQ % 2 == 0:
            g.append([0,NQ-1])
        for i in range(NQ):
            if i % 2 != 0 and i +1 != NQ:
                g.append([i,i+1])
        return g


def line_graph(NQ: int, degree: int = 2):
    g = []
    if degree == 2:
        for i in range(NQ):
            if i +1 != NQ:
                g.append([i,i+1])
    elif degree == 3:
        for i in range(NQ):
            if i +2 < NQ:
                g.append([i,i+1, i+2])
    return g



def fully_connected(NQ, degree = 2):
    g = []
    if degree == 2:
        for i in range(NQ):
            for j in range(NQ):
                if i < j:
                    g.append([i,j])
    elif degree == 3:
        for i in range(NQ):
            for j in range(NQ):
                for k in range(NQ):
                    if i < j and j < k:
                        g.append([i,j,k])
    return g
