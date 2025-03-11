from math import log2

from fineman import preprocess_graph
from fineman.dijkstra import dijkstra
from fineman.elimination_algorithm import elimination_algorithm
from fineman.helper_functions import reweight_graph


def _reverse_price_functions_on_distances(source, dists, price_function):
    actual_dists = [0] * len(dists)

    for i in range(len(actual_dists)):
        actual_dists[i] = dists[i] + price_function[i] - price_function[source]

    return actual_dists


def fineman(graph: dict[int, dict[int, int]], source: int):

    org_graph = graph.copy()
    n = len(org_graph.keys())
    m = sum(len(neighbors) for neighbors in org_graph.values())

    graph, neg_edges = preprocess_graph(org_graph, n, m)

    composed_price_function = [0] * len(graph.keys())

    n = len(graph.keys())
    neg_edges = {(u,v) for u, edges in graph.items() for v, w in edges.items() if w < 0}

    for _ in range(int(log2(n))):

        k = len(neg_edges)

        for _ in range(int(k**(2/3))):

            price_functions = elimination_algorithm(graph, neg_edges)

            for p in price_functions:
                graph, neg_edges = reweight_graph(org_graph, p)
                composed_price_function = [x + y for x, y in zip(composed_price_function, p)]

            if len(neg_edges) == 0: break

    dist = dijkstra(graph, source)

    return _reverse_price_functions_on_distances(source, dist, composed_price_function)
