from collections import deque
from math import log2
import random as rand
from numpy import inf

from bidict import bidict

from fineman import preprocess_graph
from fineman.dijkstra import dijkstra
from fineman.elimination_algorithm import elimination_algorithm
from fineman.helper_functions import reweight_graph


def _reverse_price_functions_on_distances(source, dists, price_functions):
    actual_dists = [0] * len(dists)

    for i in range(len(actual_dists)):
        actual_dists[i] = dists[i]

        for p in price_functions:
            actual_dists[i] += p[i] - p[source]

    return actual_dists

def _find_connected_component_to_source(graph, source: int):
    mapping = bidict()

    queue = deque()
    explored = [False] * len(graph)
    mapping[source] = 0
    queue.append(source)
    explored[source] = True

    new_graph = {0: {}}

    while queue:
        vertex = queue.popleft()
        if mapping[vertex] not in new_graph:
            new_graph[mapping[vertex]] = {}

        for n, w in graph[vertex].items():
            if not explored[n]:
                new_name = len(mapping)
                mapping[n] = new_name
                queue.append(n)
                explored[n] = True
            new_graph[mapping[vertex]][mapping[n]] = w

    return new_graph, mapping

def _remapping_distances(distances, n, mapping):
    dist = [inf] * n

    for old, new in mapping.items():
        dist[old] = distances[new]

    return dist


def fineman(graph: dict[int, dict[int, int]], source: int, seed = None):

    if seed is not None: rand.seed(seed)

    org_n = len(graph.keys())

    graph, index_mapping = _find_connected_component_to_source(graph, source)

    m = sum(len(neighbors) for neighbors in graph.values())
    graph, neg_edges = preprocess_graph(graph, org_n, m)

    n = len(graph.keys())
    neg_edges = {(u,v) for u, edges in graph.items() for v, w in edges.items() if w < 0}

    all_price_functions = []

    for _ in range(int(log2(n))):

        k = len(neg_edges)

        for _ in range(int(k**(2/3))):
            # TODO: consider if there is a better way to do this
            price_functions = elimination_algorithm(graph, neg_edges)
            all_price_functions = all_price_functions + price_functions

            graph, neg_edges, _ = reweight_graph(graph, price_functions)

            if len(neg_edges) == 0: break

    distances = dijkstra(graph, index_mapping[source])
    converted_distances = _reverse_price_functions_on_distances(index_mapping[source], distances, all_price_functions)

    return _remapping_distances(converted_distances, org_n, index_mapping)
