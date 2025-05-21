from numpy import inf
import heapq

def dijkstra(graph, source, org_graph):
    dist = [inf] * (len(graph.keys()))
    dist[source] = 0
    pq = []
    heapq.heappush(pq, (dist[source], source))

    org_dist = [inf] * (len(graph.keys()))
    org_dist[source] = 0

    while pq:
        current_dist, u = heapq.heappop(pq)
        if current_dist > dist[u]:
            continue

        for v in graph[u]:
            alt_dist = dist[u] + graph[u][v]
            if alt_dist < dist[v]:
                org_dist[v] = org_dist[u] + org_graph[u][v]
                dist[v] = alt_dist
                heapq.heappush(pq, (alt_dist, v))

    return org_dist
