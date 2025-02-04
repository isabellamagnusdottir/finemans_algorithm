from collections import defaultdict
import numpy as np
import random as rand

from algorithm.utils import b_hop_sssp, b_hop_stsp, super_source_bfd

def betweenness_reduction(graph,vertices,pos_edges,neg_edges,weights,tau,beta,c):
    if (beta < 1) or (tau < 1) or (tau > len(vertices)) or (c <= 1):
        raise ValueError
    rand.seed(42)

    n = len(vertices)
    sample_size = c*tau*np.ceil(np.log(n))
    T = rand.sample(vertices,sample_size)

    distances = {}
    for x in T:
        distances[x] = (b_hop_sssp(x,graph,neg_edges,weights,beta), b_hop_stsp(x,graph,weights,beta))

    h_graph, h_weights, h_neg_edges = construct_h(graph, T, distances)
    
    l = 2*sample_size

    return super_source_bfd(h_graph,h_neg_edges,h_weights,l, True)


def construct_h(graph, T, distances):
    h_graph = defaultdict(list)
    h_weights = {}
    h_neg_edges = {}

    # TODO: consider: does it require a double foor-loop?

    for t in T:
        for v in graph:
            h_graph[t].append(v)
            h_weights[(t,v)] = distances[t][1][v]
            if distances[t][1][v] < 0:
                h_neg_edges.add((t,v))

            h_graph[v].append(t)
            h_weights[(v,t)] = distances[t][2][v]
            if distances[t][2][v] < 0:
                h_neg_edges.add((t,v))
    
    return h_graph, h_weights, h_neg_edges

