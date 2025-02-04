from collections import defaultdict
import numpy as np
from queue import PriorityQueue

def dijkstra(source,graph,neg_edges,weights,dist):
    pq = PriorityQueue()

    for v in graph.keys():
        pq.put((dist[v],v))
    pq.put(dist[source],v)

    while not pq.empty():
        current_dist, u = pq.get()
        if current_dist > dist[u]:
            continue
        for v in graph[u]:
            if (u,v) in neg_edges:
                continue
            alt_dist = dist[u]+weights[(u,v)]
            if alt_dist < dist[v]:
                dist[v] = alt_dist
                pq.put((alt_dist,v))

    return dist

def bellman_ford(neg_edges,weights,dist):
    for e in neg_edges:
        (u,v) = e
        alt_dist = dist[u] + weights[(u,v)]
        if alt_dist < dist[v]:
            dist[v] = alt_dist
    return dist

def bfd(source,graph,neg_edges,weights,beta):
    dist = [np.inf]*len(graph.keys())
    dist[source] = 0
    
    dist = dijkstra(source,graph,neg_edges,weights,dist)
    for _ in range(beta):
        dist = bellman_ford(neg_edges,weights,dist)
        dist = dijkstra(source,graph,neg_edges,weights,dist)
    return dist

def b_hop_sssp(source,graph,neg_edges,weights,beta):
    return bfd(source,graph,neg_edges,weights,beta)

def b_hop_stsp(target,graph,weights,beta):
    t_graph,t_neg_edges,t_weights = transpose_graph(graph,weights)
    return b_hop_sssp(target,t_graph,t_neg_edges,t_weights,beta)

def transpose_graph(graph,weights):
    t_graph = defaultdict(list)
    t_weights = {}
    t_neg_edges = []
    for k,neighbors in graph.items():
        for v in neighbors:
            t_graph[v].append(k)
            t_weights[(v,k)] = weights[(k,v)]
            if weights[(k,v)] < 0:
                t_neg_edges.append[(v,k)]

    return t_graph,t_neg_edges,t_weights