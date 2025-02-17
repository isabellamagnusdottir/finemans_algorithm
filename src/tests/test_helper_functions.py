import numpy as np
import pytest

from fineman.helper_functions import *
from utils.load_test_case import load_test_case

TESTDATA_FILEPATH = "src/tests/test_data/graphs/"

@pytest.mark.parametrize("filename", [
    "complete_4_vertices_graph_with_no_neg_edges.json",
    "graph_already_adhere_to_one_degree_restriction.json",
    "high_in_degree_graph.json",
    "small_graph_with_neg_edges.json",
    "tree_graph_single_root_with_100_children.json",
    "graph_with_no_edges.json",
    "disconnected_graph.json",
    "path_with_only_neg_edges.json"
])
def test_transpose_graph_on_multiple_graphs(filename):
    graph, _ = load_test_case(TESTDATA_FILEPATH + filename)

    transposed_graph, _ = transpose_graph(graph)

    assert graph.keys() == transposed_graph.keys()
    assert all(all(graph[neighbor][vertex]  == weight for neighbor, weight in neighbors.items()) for vertex, neighbors in transposed_graph.items())

    org_graph, _ = transpose_graph(transposed_graph)
    assert graph == org_graph


@pytest.mark.parametrize("filename,expected", [
    ("complete_4_vertices_graph_with_no_neg_edges.json", []),
    ("disconnected_graph.json", [1,4]),
    ("graph_with_no_edges.json", []),
    ("small_graph_with_neg_edges.json", [1,3])
])
def test_negative_vertices_set(filename, expected):
    graph, _ = load_test_case(TESTDATA_FILEPATH + filename)
    actual = get_set_of_neg_vertices(graph)
    assert actual == set(expected)


@pytest.mark.parametrize("filename,expected", [
    ("complete_4_vertices_graph_with_no_neg_edges.json", [np.inf, 0, 1, 1, 1]),
    ("disconnected_graph.json", [np.inf, 0, 1, 2, np.inf, np.inf, np.inf]),
    ("path_with_only_neg_edges.json", [np.inf, 0, np.inf, np.inf, np.inf, np.inf, np.inf]),
    ("small_graph_with_neg_edges.json", [np.inf, 0, 5, 11, np.inf, 6, 7]),
    ("graph_with_no_edges.json", [np.inf, 0, np.inf, np.inf, np.inf, np.inf, np.inf]),
    ("path_tricky.json", [np.inf, 0, 0, 10, 10, 10, 10])
])
def test_dijkstra_implementation(filename, expected):
    graph, neg_edges = load_test_case(TESTDATA_FILEPATH + filename)

    initial_dist = [np.inf]*(len(graph.keys())+1)
    initial_dist[1] = 0

    dist = dijkstra(graph, neg_edges, initial_dist)
    assert dist == expected


@pytest.mark.parametrize("filename,expected", [
    ("complete_4_vertices_graph_with_no_neg_edges.json", [np.inf, 0, np.inf, np.inf, np.inf]),
    ("disconnected_graph.json", [np.inf, 0, np.inf, -1, np.inf, np.inf, np.inf]),
    ("path_with_only_neg_edges.json", [np.inf, 0, -1, np.inf, np.inf, np.inf, np.inf]),
    ("path_tricky.json", [np.inf, 0, np.inf, np.inf, np.inf, np.inf, np.inf]),
])
def test_bellman_ford_implementation(filename, expected):
    graph, neg_edges = load_test_case(TESTDATA_FILEPATH + filename)

    initial_dist = [np.inf]*(len(graph.keys())+1)
    initial_dist[1] = 0

    dist = bellman_ford(graph, neg_edges, initial_dist)
    assert dist == expected


@pytest.mark.parametrize("filename,beta,expected", [
    ("graph_with_no_edges.json", 1, [np.inf, 0, np.inf, np.inf, np.inf, np.inf, np.inf]),
    ("disconnected_graph.json", 0, [np.inf, 0, 1, 2, np.inf, np.inf, np.inf]),
    ("disconnected_graph.json", 1, [np.inf, 0, 1, -1, np.inf, np.inf, np.inf]),
    ("path_with_only_neg_edges.json", 0, [np.inf, 0, np.inf, np.inf, np.inf, np.inf, np.inf]),
    ("path_with_only_neg_edges.json", 1, [np.inf, 0, -1, np.inf, np.inf, np.inf, np.inf]),
    ("path_with_only_neg_edges.json", 2, [np.inf, 0, -1, -2, np.inf, np.inf, np.inf]),
    ("path_with_only_neg_edges.json", 3, [np.inf, 0, -1, -2, -3, np.inf, np.inf]),
    ("small_graph_with_neg_edges.json", 0, [np.inf, 0, 5, 11, np.inf, 6, 7]),
    ("small_graph_with_neg_edges.json", 1, [np.inf, 0, 5, 11, -2, 0, 1]),
    ("graph_with_neg_edges.json", 0, [np.inf, 0, 3, 25, 7, np.inf, 11, 16, np.inf, np.inf, 20, np.inf, np.inf, np.inf, 19]),
    ("graph_with_neg_edges.json", 1, [np.inf, 0, 3, -6, 7, 5, 11, 8, 1, 2, 20, 4, 6, 11, 11]),
    ("graph_with_neg_edges.json", 2, [np.inf, 0, 3, -6, 7, -7, 11, -5, 1, -11, 20, -9, 6, -2, -2]),
    ("graph_with_neg_edges.json", 3, [np.inf, 0, 3, -6, 7, -7, 11, -5, 1, -11, 20, -9, 6, -2, -2]),
    ("path_tricky.json", 0, [np.inf, 0, 0, 10, 10, 10, 10]),
    ("path_tricky.json", 1, [np.inf, 0, 0, -1, 9, 9, 9]),
    ("path_tricky.json", 2, [np.inf, 0, 0, -1, -2, 8, 8]),
    ("path_tricky.json", 3, [np.inf, 0, 0, -1, -2, -3, 7]),
    ("path_tricky.json", 4, [np.inf, 0, 0, -1, -2, -3, -4]),
])
def test_beta_hop_sssp_implementation(filename, beta, expected):
    graph, neg_edges = load_test_case(TESTDATA_FILEPATH + filename)

    dist = b_hop_sssp(1, graph, neg_edges, beta)
    assert dist == expected


@pytest.mark.parametrize("filename,beta,expected", [
    ("graph_with_no_edges.json", 1, [np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, 0]),
    ("disconnected_graph.json", 0, [np.inf, np.inf, np.inf, np.inf, 2, 1, 0]),
    ("disconnected_graph.json", 1, [np.inf, np.inf, np.inf, np.inf, 0, 1, 0]),
    ("path_with_only_neg_edges.json", 0, [np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, 0]),
    ("path_with_only_neg_edges.json", 1, [np.inf, np.inf, np.inf, np.inf, np.inf, -1, 0]),
    ("path_with_only_neg_edges.json", 2, [np.inf, np.inf, np.inf, np.inf, -2, -1, 0]),
    ("path_with_only_neg_edges.json", 3, [np.inf, np.inf, np.inf, -3, -2, -1, 0]),
    ("small_graph_with_neg_edges.json", 0, [np.inf, 7, 10, 4, 3, 1, 0]),
    ("small_graph_with_neg_edges.json", 1, [np.inf, 1, 4, -2, 3, 1, 0]),
    ("graph_with_neg_edges.json", 0, [np.inf, 19, np.inf, np.inf, 12, 8, 8, 3, 10, 9, np.inf, 7, np.inf, 10, 0]),
    ("graph_with_neg_edges.json", 1, [np.inf, 11, 8, 4, 6, 8, 5, 3, 10, 9, -4, 7, 7, 10, 0]),
    ("graph_with_neg_edges.json", 2, [np.inf, -2, 8, 4, 6, 8, 5, 3, 10, 9, -4, 7, 7, 10, 0]),
    ("graph_with_neg_edges.json", 3, [np.inf, -2, 8, 4, 6, 8, 5, 3, 10, 9, -4, 7, 7, 10, 0]),
    ("path_tricky.json", 0, [np.inf, 10, np.inf, np.inf, np.inf, np.inf, 0]),
    ("path_tricky.json", 1, [np.inf, 9, np.inf, np.inf, np.inf, -1, 0]),
    ("path_tricky.json", 2, [np.inf, 8, np.inf, np.inf, -2, -1, 0]),
    ("path_tricky.json", 3, [np.inf, 7, np.inf, -3, -2, -1, 0]),
    ("path_tricky.json", 4, [np.inf, -4, -4, -3, -2, -1, 0]),
    ("path_tricky.json", 5, [np.inf, -4, -4, -3, -2, -1, 0]),
])
def test_beta_hop_stsp_implementation(filename, beta, expected):
    graph, _ = load_test_case(TESTDATA_FILEPATH + filename)

    dist = b_hop_stsp(len(graph.keys()), graph, beta)
    assert dist == expected


@pytest.mark.parametrize("filename,beta,expected", [
    ("graph_with_no_edges.json", 0, [np.inf, 0, 0, 0, 0, 0, 0]),
    ("disconnected_graph.json", 0, [np.inf, 0, 0, 0, 0, 0, 0]),
    ("disconnected_graph.json", 1, [np.inf, 0, 0, -1, 0, -1, 0]),
    ("path_with_only_neg_edges.json", 0, [np.inf, 0, 0, 0, 0, 0, 0]),
    ("path_with_only_neg_edges.json", 1, [np.inf, 0, -1, -1, -1, -1, -1]),
    ("path_with_only_neg_edges.json", 2, [np.inf, 0, -1, -2, -2, -2, -2]),
    ("path_with_only_neg_edges.json", 3, [np.inf, 0, -1, -2, -3, -3, -3]),
    ("path_with_only_neg_edges.json", 4, [np.inf, 0, -1, -2, -3, -4, -4]),
    ("path_tricky.json", 0, [np.inf, 0, 0, 0, 0, 0, 0]),
    ("path_tricky.json", 1, [np.inf, 0, 0, -1, -1, -1, -1]),
    ("path_tricky.json", 2, [np.inf, 0, 0, -1, -2, -2, -2]),
    ("small_graph_with_neg_edges.json", 1, [np.inf, 0, 0, 0, -2, -3, -2]),
    ("graph_with_neg_edges.json", 1, [np.inf, 0, 0, -6, 0, -2, 0, 0, -2, -5, 0, -3, 0, -3, -4]),
    ("graph_with_neg_edges.json", 2, [np.inf, 0, 0, -6, 0, -7, 0, -5, -2, -11, 0, -9, 0, -3, -4]),
    ("graph_with_neg_edges.json", 3, [np.inf, 0, 0, -6, 0, -7, 0, -5, -2, -11, 0, -9, 0, -3, -4])
])
def test_super_source_bfd_without_cycle_detection(filename, beta, expected):
    graph, neg_edges = load_test_case(TESTDATA_FILEPATH + filename)

    dist = super_source_bfd(graph, neg_edges, beta)
    assert dist == expected


@pytest.mark.parametrize("filename,beta,expected", [
    ("small_graph_with_neg_edges.json", 1, [np.inf, 0, 0, 0, -2, -3, -2]),
    ("graph_with_neg_edges.json", 2, [np.inf, 0, 0, -6, 0, -7, 0, -5, -2, -11, 0, -9, 0, -3, -4]),
])
def test_super_source_bfd_cycle_detection_on_graphs_without_neg_cycles(filename, beta, expected):
    graph, neg_edges = load_test_case(TESTDATA_FILEPATH + filename)
    dist = super_source_bfd(graph, neg_edges, beta, cycleDetection=True)
    assert dist == expected


@pytest.mark.parametrize("filename,beta", [
    ("negative_cycle_4.json", 1),
    ("negative_cycle_4.json", 2),
    ("negative_cycle_4.json", 3),
    ("graph_with_neg_cycle.json", 2),
    ("graph_with_neg_cycle.json", 3),
    ("graph_with_neg_cycle.json", 10)
])
def test_super_source_bfd_cycle_detection_on_graphs_with_neg_cycles(filename, beta):
    graph, neg_edges = load_test_case(TESTDATA_FILEPATH + filename)
    with pytest.raises(ValueError):
        super_source_bfd(graph, neg_edges, beta, cycleDetection=True)


@pytest.mark.parametrize("source,mid,target,beta,expected", [
    (1,2,8,0,np.inf),
    (1,3,8,0,np.inf),
    (1,4,8,0,np.inf),
    (1,2,8,1,-1),
    (1,3,8,1,-4),
    (1,4,8,1,-5),
    (1,5,8,1,-1),
    (1,6,8,1,-4),
    (1,7,8,1,-5),
    (1,7,8,2,-5)
])
def test_through_dist_small_flow_dag(source,mid,target,beta,expected):
    graph,neg_edges = load_test_case(TESTDATA_FILEPATH+"small_flow_dag.json")
    actual = compute_throughdist(source,mid,target,graph,neg_edges,beta)
    assert actual == expected


@pytest.mark.parametrize("source,mid,target,beta,expected", [
   (1,2,1,0,np.inf),
   (1,2,1,1,np.inf),
   (1,2,1,2,12),
   (1,3,6,1,np.inf),
   (1,3,6,2,5)
])
def test_through_dist_small_pos_cycle(source,mid,target,beta,expected):
    graph,neg_edges = load_test_case(TESTDATA_FILEPATH+"small_pos_cycle.json")
    actual = compute_throughdist(source,mid,target,graph,neg_edges,beta)
    assert actual == expected


@pytest.mark.parametrize("source,mid,target,beta,expected", [
   (1,2,1,0,np.inf),
   (1,2,1,1,np.inf),
   (1,2,1,2,np.inf),
   (1,2,1,3,np.inf),
   (1,2,1,4,np.inf),
   (1,2,1,5,-26),
   (1,4,1,2,np.inf),
   (1,4,1,3,-26)
])
def test_through_dist_small_negative_cycle(source,mid,target,beta,expected):
    graph,neg_edges = load_test_case(TESTDATA_FILEPATH+"negative_cycle_6.json")
    actual = compute_throughdist(source,mid,target,graph,neg_edges,beta)
    assert actual == expected

@pytest.mark.parametrize("source,mid,target,beta,expected", [
   (1,3,6,0,np.inf),
   (1,3,6,1,np.inf),
   (1,3,6,2,np.inf),
   (1,3,6,3,-5)
])
def test_through_dist_small_negative_path(source,mid,target,beta,expected):
    graph,neg_edges = load_test_case(TESTDATA_FILEPATH+"path_with_only_neg_edges.json")
    actual = compute_throughdist(source,mid,target,graph,neg_edges,beta)
    assert actual == expected


@pytest.mark.parametrize("source,mid,target,beta,expected", [
   (1,3,6,0,5)
])
def test_through_dist_small_positive_path(source,mid,target,beta,expected):
    graph,neg_edges = load_test_case(TESTDATA_FILEPATH+"path_with_only_positive_edges.json")
    actual = compute_throughdist(source,mid,target,graph,neg_edges,beta)
    assert actual == expected


@pytest.mark.parametrize("source,target,beta,expected", [
    (1,8,0,set()),
    (1,8,1,{1,2,3,4,5,6,7,8}),
    (1,5,1,{1,2,5}),
    (1,6,1,{1,3,6}),
    (1,7,1,{1,4,7}),
    (2,5,1,{2,5})
])

def test_betweenness_set_small_flow_dag(source,target,beta,expected):
    graph,neg_edges = load_test_case(TESTDATA_FILEPATH+"small_flow_dag.json")
    actual = find_betweenness_set(source,target,graph,neg_edges,beta)
    assert actual == expected

@pytest.mark.parametrize("beta,expected", [
    (0, set()),
    (1, {10, 16, 19, 20, 21, 24}),
    (2, {1, 4, 5, 7, 10, 11, 12, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25}),
    (3, {1, 2, 4, 5, 6, 7, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25})
])
def test_betweenness_set_flow_dag_with_source_1_and_target_25(beta, expected):
    graph, neg_edges = load_test_case(TESTDATA_FILEPATH + "dag_flow.json")
    actual = find_betweenness_set(1, 25, graph, neg_edges, beta)
    assert actual == expected

@pytest.mark.parametrize("beta,expected", [
    (0, set()),
    (1, {3}),
    (2, {1, 3, 7, 9, 11, 14}),
    (3, {1, 3, 7, 9, 11, 14})
])
def test_betweenness_set_random_graph_with_neg_edges_with_source_1_and_target_15(beta, expected):
    graph, neg_edges = load_test_case(TESTDATA_FILEPATH + "graph_with_neg_edges.json")
    actual = find_betweenness_set(1, 14, graph, neg_edges, beta)
    assert actual == expected

@pytest.mark.parametrize("source,target,beta,expected", [
    (1,1,1,set()),
    (1,1,2,{3}),
    (1,1,3,{2,3,4}),
    (1,1,4,{1,2,3,4})
])
def test_betweenness_set_negative_cycle4(source, target, beta, expected):
    graph, neg_edges = load_test_case(TESTDATA_FILEPATH + "negative_cycle_4.json")
    actual = find_betweenness_set(source, target, graph, neg_edges, beta)
    assert actual == expected

@pytest.mark.parametrize("source,target,beta,expected", [
    (1, 4, 1, set()),
    (1, 4, 2, set()),
    (1, 4, 3, {3}),
    (1, 4, 4, {1, 2, 3, 4}),
    (4, 1, 2, {1, 2, 3, 4})
])
def test_betweenness_set_complete_graph_with_neg_edges(source, target, beta, expected):
    graph, neg_edges = load_test_case(TESTDATA_FILEPATH + "complete_4_vertices_graph_with_neg_edges.json")
    actual = find_betweenness_set(source, target, graph, neg_edges, beta)
    assert actual == expected


@pytest.mark.parametrize("source,target,beta,expected", [
    (1,8,0,set()),
    (1,8,1,{1,2,4,8}),
    (1,23,0,set()),
    (1,23,1,{13,22}),
    (1,18,0,set()),
    (1,18,1,{14}),
    (1,19,0,set()),
    (1,19,1,set()),
    (1,19,2,{11,15}),
    (1,20,0,set()),
    (1,20,1,set()),
    (1,21,0,set()),
    (1,21,1,{12,17})
])
def test_betweeness_set_small_tree_with_negative_edges_from_root_to_leaves(source,target,beta,expected):
    graph,neg_edges = load_test_case(TESTDATA_FILEPATH+"small_tree.json")
    actual = find_betweenness_set(source,target,graph,neg_edges,beta)
    assert actual == expected


@pytest.mark.parametrize("source,target,beta,expected", [
    (1,1,0,set()),
    (1,2,0,set()),
    (1,2,1,{1,2}),
    (1,3,1,{2}),
    (1,3,2,{1,2,3}),
    (1,6,2,set()),
    (1,6,3,{3,4}),
    (1,6,4,{2,3,4,5}),
    (1,6,5,{1,2,3,4,5,6})
])
def test_betweeness_set_small_path_with_only_negative_edges(source,target,beta,expected):
    graph,neg_edges = load_test_case(TESTDATA_FILEPATH+"path_with_only_neg_edges.json")
    actual = find_betweenness_set(source,target,graph,neg_edges,beta)
    assert actual == expected

@pytest.mark.parametrize("source,target,beta,expected", [
    (1,6,0,set()),
    (1,6,100,set())
])
def test_betweeness_set_small_path_with_only_positive_edges(source,target,beta,expected):
    graph,neg_edges = load_test_case(TESTDATA_FILEPATH+"path_with_only_positive_edges.json")
    actual = find_betweenness_set(source,target,graph,neg_edges,beta)
    assert actual == expected

@pytest.mark.parametrize("source,mid,target,beta,expected", [
   (1,2,1,0,np.inf),
   (1,2,1,1,np.inf),
   (1,2,1,2,np.inf),
   (1,2,1,3,np.inf),
   (1,2,1,4,np.inf),
   (1,2,1,5,-26),
   (1,4,1,2,np.inf),
   (1,4,1,3,-26)
])
def test_through_dist_on_negative_cycle(source,mid,target,beta,expected):
    graph,neg_edges = load_test_case(TESTDATA_FILEPATH+"negative_cycle_6.json")
    actual = compute_throughdist(source,mid,target,graph,neg_edges,beta)
    assert actual == expected

@pytest.mark.parametrize("source,target,beta,expected", [
    (1,8,0,set()),
    (1,8,1,set()),
    (1,8,2,set()),
    (1,8,3,{4}),
    (1,8,4,{1,2,3,4,7,8}),
    (1,8,5,{1,2,3,4,6,7,8,9}),
    (2,8,1,{6,9}),
    (1,5,4,set()),
    (1,5,5,{6,9}),
    (1,5,6,{1,2,3,5,6,7,8,9}),
    (1,5,7,{1,2,3,4,5,6,7,8,9})

])
def test_betweenness_set_grid_with_negative_edges(source,target,beta,expected):
    graph,neg_edges = load_test_case(TESTDATA_FILEPATH+"small_grid_with_negative_edges.json")
    actual = find_betweenness_set(source,target,graph,neg_edges,beta)
    assert actual == expected

@pytest.mark.parametrize("price_function,expected", [
    ([0,2,2,2,2,2,2],
     {1: {2: 1},2: {3: 1}, 3:{4: 1}, 4:{5: 1},5: {6: 1},6:{}}),
    ([0,2,-2,2,-2,2,-2],
     {1: {2: 5},2: {3: -3}, 3:{4: 5}, 4:{5: -3},5: {6: 5},6:{}}),
    ([0,-2,7,-9,0,6,3],
     {1: {2: -8},2: {3: 17}, 3:{4: -8}, 4:{5: -5},5: {6: 4},6:{}}),
])
def test_reweight_path_given_price_function(price_function, expected):
    graph,_ = load_test_case(TESTDATA_FILEPATH+"path_with_only_positive_edges.json")
    assert reweight_graph(graph,price_function) == expected

@pytest.mark.parametrize("price_function,expected", [
    ([0,-3,5,-7,-1],
     {1: {2: -9},2: {3: 11}, 3:{4: -7}, 4:{1: 1}}),
])
def test_reweight_cycle_given_price_function(price_function, expected):
    graph,_ = load_test_case(TESTDATA_FILEPATH+"negative_cycle_4.json")
    assert reweight_graph(graph,price_function) == expected