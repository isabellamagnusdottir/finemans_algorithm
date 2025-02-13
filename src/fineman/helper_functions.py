import numpy as np
from queue import PriorityQueue

def dijkstra(graph: dict[int, dict[int, int]], neg_edges: set, dist: list):
    pq = PriorityQueue()

    for v in graph.keys():
        pq.put((dist[v], v))

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


# hold styr på hvorvidt vægten, som står der nu, kommer fra den nuværende bellman-ford eller fra tidligere
def bellman_ford(graph : dict[int, dict[int, int]], neg_edges: set, dist: list):

    old_dist = dist.copy()
    # TODO: consider it a dict from vertex to bool is better? depends on the ratio between neg_edges and all edges
    used_hop_in_round = [False] * (len(graph.keys())+1)

    for (u,v) in neg_edges:
        alt_dist = dist[u] + graph[u][v]

        if used_hop_in_round[u]:
            alt_dist = old_dist[u] + graph[u][v]

        if alt_dist < dist[v]:
            dist[v] = alt_dist
            used_hop_in_round[v] = True
    return dist

def bfd(graph, neg_edges, dist: list, beta: int):
    dist = dijkstra(graph, neg_edges, dist)
    for _ in range(beta):
        dist = bellman_ford(graph, neg_edges, dist)
        dist = dijkstra(graph, neg_edges, dist)
    return dist

def b_hop_sssp(source, graph: dict[int, dict[int, int]], neg_edges: set, beta):
    dist = [np.inf]*(len(graph.keys())+1)
    dist[source] = 0

    return bfd(graph, neg_edges, dist, beta)

def b_hop_stsp(target, graph: dict[int, dict[int, int]], beta):
    t_graph, t_neg_edges = transpose_graph(graph)
    return b_hop_sssp(target, t_graph, t_neg_edges, beta)

def transpose_graph(graph: dict[int, dict[int, int]]):
    t_graph = {}
    t_neg_edges = set()

    for k, neighbors in graph.items():
        if k not in t_graph:
            t_graph[k] = {}

        for v, w in neighbors.items():
            if v not in t_graph:
                t_graph[v] = {}
            
            t_graph[v][k] = w
            
            if w < 0:
                t_neg_edges.add((v,k))

    return t_graph, t_neg_edges

# TODO: consider refactoring cycle detection
def super_source_bfd(graph: dict[int, dict[int, int]], neg_edges: set, beta, cycleDetection = False):

    super_source = len(graph)+1
    graph[super_source] = {}
    for v in range(1, len(graph)):
        graph[super_source][v] = 0

    distances1 = b_hop_sssp(super_source, graph, neg_edges, beta)
    if cycleDetection:
        distances2 = bfd(graph, neg_edges, distances1.copy(), beta)
        
        for v in graph.keys():
            if distances2[v] < distances1[v]:
                # TODO: implement cycle error
                raise ValueError
 
    return distances1[:-1]

def get_set_of_neg_vertices(graph: dict[int, dict[int, int]]):
    neg_vertices = set()

    for vertex, edge in graph.items():
        for weight in edge.values():
            if weight < 0:
                neg_vertices.add(vertex)
    
    return neg_vertices
