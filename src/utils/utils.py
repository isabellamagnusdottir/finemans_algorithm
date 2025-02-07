import numpy as np
from queue import PriorityQueue

def dijkstra(source, graph: dict[int, set[tuple[int, int]]], neg_edges, dist):
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
            alt_dist = dist[u]+graph[u][v]
            if alt_dist < dist[v]:
                dist[v] = alt_dist
                pq.put((alt_dist,v))

    return dist

def bellman_ford(graph : dict[int, set[tuple[int, int]]], neg_edges,dist):
    for e in neg_edges:
        (u,v) = e
        alt_dist = dist[u] + graph[u][v]
        if alt_dist < dist[v]:
            dist[v] = alt_dist
    return dist

def bfd(source, graph, neg_edges, dist, beta):
    dist = dijkstra(source, graph, neg_edges, dist)
    for _ in range(beta):
        dist = bellman_ford(graph, neg_edges, dist)
        dist = dijkstra(source, graph, neg_edges, dist)
    return dist

def b_hop_sssp(source, graph, neg_edges, beta):
    dist = [np.inf]*len(graph.keys())
    dist[source] = 0
    return bfd(source, graph, neg_edges, beta)

def b_hop_stsp(target, graph, beta):
    t_graph, t_neg_edges = transpose_graph(graph)
    return b_hop_sssp(target, t_graph, t_neg_edges, beta)

def transpose_graph(graph: dict[int, set[tuple[int, int]]]):
    t_graph = {}
    t_neg_edges = set()

    for k, neighbors in graph.items():
        if k not in t_graph:
            t_graph[k] = set()

        for v, w in neighbors:
            if v not in t_graph:
                t_graph[v] = set()
            
            t_graph[v].add((k,w))
            
            if w < 0:
                t_neg_edges.add((v,k))

    return t_graph, t_neg_edges

# TODO: consider refactoring cycle detection
def super_source_bfd(graph, neg_edges, beta, cycleDetection = False):

    super_source = len(graph)
    for v in graph:
        graph[super_source].add((v,0))

    distances1 = b_hop_sssp(super_source, graph, neg_edges, beta)
    if cycleDetection:
        distances2 = bfd(super_source, graph, neg_edges, distances1, beta)
        
        for v in graph.keys():
            if distances2[v] < distances1[v]:
                # TODO: implement cycle error
                raise ValueError
 
    return distances1

def get_set_of_neg_vertices(graph):
    neg_vertices = set()

    for vertex, edge in graph.items():
        for _, weight in edge:
            if weight < 0:
                neg_vertices.add(vertex)
    
    return neg_vertices
