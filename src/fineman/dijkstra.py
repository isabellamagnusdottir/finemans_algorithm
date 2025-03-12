from queue import PriorityQueue
from numpy import inf
from src.utils.cycle_error import NegativeCycleError

def dijkstra(graph, source):
    dist = [inf] * (len(graph.keys()))
    dist[source] = 0
    #predecessor = [-1] * len(graph.keys())

    pq = PriorityQueue()

    for v in graph.keys():
        pq.put((dist[v], v))

    while not pq.empty():
        current_dist, u = pq.get()
        if current_dist > dist[u]:
            continue

        for v in graph[u]:
            alt_dist = dist[u] + graph[u][v]
            if alt_dist < dist[v]:
                dist[v] = alt_dist
                pq.put((alt_dist, v))
                #predecessor[v] = u

    d = False
    if d:
        raise NegativeCycleError

    return dist #, predecessor
