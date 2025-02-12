import numpy as np
import pytest

from fineman.helper_functions import *
from utils.load_test_case import load_test_case

TESTDATA_FILEPATH = "src/tests/test_data/"

@pytest.mark.parametrize("filename", [
    "complete_four_vertices_graph_with_no_neg_edges.json",
    "graph_already_adhere_to_one_degree_restriction.json",
    "high_in_degree_graph.json",
    "small_graph_with_neg_edges.json",
    "tree_graph_single_root_with_100_children.json",
    "graph_with_no_edges.json",
    "disconnected_graph.json"
])
def test_transpose_graph_on_multiple_graphs(filename):
    graph = load_test_case(TESTDATA_FILEPATH + filename)

    transposed_graph, _ = transpose_graph(graph)

    assert graph.keys() == transposed_graph.keys()
    assert all(all(graph[neighbor][vertex]  == weight for neighbor, weight in neighbors.items()) for vertex, neighbors in transposed_graph.items())

    org_graph, _ = transpose_graph(transposed_graph)
    assert graph == org_graph


@pytest.mark.parametrize("filename,expected", [
    ("complete_four_vertices_graph_with_no_neg_edges.json", []),
    ("disconnected_graph.json", [1,4]),
    ("graph_with_no_edges.json", []),
    ("small_graph_with_neg_edges.json", [1,3])
])
def test_negative_vertices_set(filename, expected):
    graph = load_test_case(TESTDATA_FILEPATH + filename)
    actual = get_set_of_neg_vertices(graph)

    assert actual == set(expected)

@pytest.mark.parametrize("filename,expected", [
    ("complete_four_vertices_graph_with_no_neg_edges.json", {1:0, 2:1, 3:1, 4:1}),
    ("disconnected_graph.json", {1:0, 2:1, 3:2, 4:np.inf, 5:np.inf, 6: np.inf}),
    ("small_graph_with_neg_edges.json", {1:0, 2:5, 3:11, 4:np.inf, 5:6, 6:7}),
    ("graph_with_no_edges.json", {1: 0, 2:np.inf, 3:np.inf, 4:np.inf, 5:np.inf, 6: np.inf}),
])
def test_dijkstra_implementation(filename, expected):
    graph = load_test_case(TESTDATA_FILEPATH + filename)

    initial_dist = {v:np.inf for v in graph.keys()}
    initial_dist[1] = 0

    neg_edges = [(u, v) for u, neighbors in graph.items() for v, weight in neighbors.items() if weight < 0]

    dist = dijkstra(1, graph, neg_edges, initial_dist)
    assert dist == expected


@pytest.mark.parametrize("filename,expected", [
    ("complete_four_vertices_graph_with_no_neg_edges.json", {1:0, 2:np.inf, 3:np.inf, 4:np.inf}),
    ("disconnected_graph.json", {1:0, 2:np.inf, 3:-1, 4:np.inf, 5:np.inf, 6:np.inf}),
])
def test_bellman_ford_implementation(filename, expected):
    graph = load_test_case(TESTDATA_FILEPATH + filename)

    initial_dist = {v: np.inf for v in graph.keys()}
    initial_dist[1] = 0

    neg_edges = [(u, v) for u, neighbors in graph.items() for v, weight in neighbors.items() if weight < 0]

    dist = bellman_ford(graph, neg_edges, initial_dist)
    assert dist == expected