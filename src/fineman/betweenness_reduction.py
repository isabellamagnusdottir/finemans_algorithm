from math import ceil, log
import random as rand
from src.fineman.helper_functions import h_hop_sssp, h_hop_stsp, super_source_bfd

def betweenness_reduction(graph: dict[int, dict[int, float]], neg_edges, tau, beta, c, seed = None):
    if (beta < 1) or (tau < 1) or (tau > len(graph)) or (c <= 1):
        raise ValueError("Invalid parameter")

    if seed is not None:
        rand.seed(seed)

    n = len(graph)
    sample_size = int(c*tau*ceil(log(n)))
    if sample_size > len(graph):
        sample_size = len(graph)

    T = rand.sample(tuple(graph.keys()), sample_size)

    distances = {}
    for x in T:
        distances[x] = (h_hop_sssp(x, graph, neg_edges, beta), h_hop_stsp(x, graph, beta))

    h_graph, h_neg_edges = _construct_h(graph, T, distances)
    
    l = 2*sample_size

    return super_source_bfd(h_graph, h_neg_edges, l, cycleDetection=True)


def _construct_h(graph: dict[int, dict[int, float]], T, distances):
    h_graph = {}
    h_neg_edges = set()

    for v in graph.keys():
        if v not in h_graph:
            h_graph[v] = {}

        for t in T:
            if v == t:
                continue

            if t not in h_graph:
                h_graph[t] = {}

            h_graph[t][v] = distances[t][0][v]
            if distances[t][0][v] < 0:
                h_neg_edges.add((t,v))

            h_graph[v][t] = distances[t][1][v]
            if distances[t][1][v] < 0:
                h_neg_edges.add((v,t))
    
    return h_graph, h_neg_edges
