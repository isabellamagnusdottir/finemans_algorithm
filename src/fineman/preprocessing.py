from math import ceil
from collections import deque
from src.fineman.core_functions import get_set_of_neg_vertices, transpose_graph
from src.utils.threshold_error import InvalidThresholdError
import src.globals as globals

SCALAR_FOR_THRESHOLD = 4

def ensure_simp1(graph: dict[int, dict[int, float]]):
    
    n = len(graph.keys())
    neg_vertices = get_set_of_neg_vertices(graph)

    for vertex in neg_vertices:
        if len(graph[vertex]) > 1:
            
            old_neighbors = graph[vertex]

            # introduce new vertex
            new_vertex = n
            n = n + 1
            most_neg_weight = min(weights for weights in graph[vertex].values())
            graph[vertex] = {new_vertex: most_neg_weight}

            # change weights on existing edges
            graph[new_vertex] = {}
            for neighbor, weight in old_neighbors.items():
                graph[new_vertex][neighbor] = weight - most_neg_weight

    return graph


def ensure_simp2(graph: dict[int, dict[int, float]], threshold: int):

    n = len(graph.keys())

    split_queue = deque()

    for vertex in graph.keys():
        if len(graph[vertex]) > threshold:
            split_queue.append(vertex)

    while split_queue:
        vertex = split_queue.popleft()

        new_vertex1, new_vertex2 = n, n+1
        n = n + 2
        graph[new_vertex1] = {}
        graph[new_vertex2] = {}

        mid = ceil(len(graph[vertex])/2)

        # halve edges
        count = 0
        for v, w in graph[vertex].items():
            if count < mid:
                graph[new_vertex1][v] = w
            else:
                graph[new_vertex2][v] = w
            count += 1


        graph[vertex] = {new_vertex1:globals.WEIGHT_TYPE(0), new_vertex2:globals.WEIGHT_TYPE(0)}

        # check whether new vertices violate the degree threshold
        if len(graph[new_vertex1]) > threshold:
            split_queue.append(new_vertex1)

            if len(graph[new_vertex2]) > threshold:
                split_queue.append(new_vertex2)

    return graph


def compute_threshold(n: int, m: int):
    threshold = ceil((m / n)) * SCALAR_FOR_THRESHOLD

    if threshold <= 2:
        raise InvalidThresholdError
    
    return threshold


def preprocess_graph(graph: dict[int, dict[int, float]], n, m):

    threshold = compute_threshold(n, m)

    transformed_graph = ensure_simp1(graph)

    # ensure for out-degree
    transformed_graph = ensure_simp2(transformed_graph, threshold)

    # ensure for in-degree
    transposed_graph, _ = transpose_graph(transformed_graph)
    final_transposed_graph = ensure_simp2(transposed_graph, threshold)
    
    return transpose_graph(final_transposed_graph)

