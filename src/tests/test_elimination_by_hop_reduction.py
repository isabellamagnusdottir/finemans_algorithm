import pytest

from src.fineman.elimination_by_hop_reduction import _construct_h, _elimination_by_hop_reduction
from src.utils import load_test_case, NegativeCycleError

TESTDATA_FILEPATH = "src/tests/test_data/graphs/"

@pytest.mark.parametrize("filename",[
    "small_flow_dag.json",
    "dag_flow.json",
    "disconnected_graph.json",
    "complete_4_vertices_graph_with_neg_edges.json"
])
def test_construction_of_h_with_empty_R_set(filename):
    graph, neg_edges = load_test_case(TESTDATA_FILEPATH + filename)

    h, actual_neg_edges, mapping = _construct_h(graph, neg_edges, [[0] * len(graph)], set(), 0)

    expected_neg_edges = {(u,v) for u, edges in h.items() for v, w in edges.items()  if w < 0}

    assert graph == h
    assert expected_neg_edges == actual_neg_edges


@pytest.mark.parametrize("dists,R_set,r,expected_h", [
    ([[0,0,0,0,0,0,0,0], [0,0,0,0,-3,-7,-9,-8]], {1,2,5}, 1, {(0,0): {(1,0): 1, (2,0): 2, (3,0): 3},
                                                              (1,0): {(1,1): 0, (4,0): -3},
                                                              (1,1): {(1,0): 0}, (2,0): {(2,1): 0,(5,1): 0},
                                                              (2,1): {(2,0): 0}, (3,0): {(6,0): -9},
                                                              (4,0): {(7,0): 1}, (5,0): {(5,1): 7,(7,0): 1},
                                                              (5,1): {(5,0): -7, (7,0): -6},
                                                              (6,0): {(7,0): 1}, (7,0): {}}
     ),
    ([[0,0,0,0,0,0,0,0],[0,0,0,0,-3,-7,-9,-8],[0,0,0,0,-3,-7,-9,-8]], {1,2,5}, 2, {(0,0): {(1,0): 1,(2,0): 2,(3,0): 3},
                                                                                    (1,0): {(1,1): 0, (4,0): -3},
                                                                                    (1,1): {(1,2): 0, (4,0): -3},
                                                                                    (1,2): {(1,0): 0},
                                                                                    (2,0): {(2,1): 0, (5,1): 0},
                                                                                    (2,1): {(2,2): 0, (5,2): 0},
                                                                                    (2,2): {(2,0): 0},
                                                                                    (3,0): {(6,0): -9}, (4,0): {(7,0): 1},
                                                                                    (5,0): {(5,1): 7, (7,0): 1},
                                                                                    (5,1): {(5,2): 0, (7,0): -6},
                                                                                    (5,2): {(5,0): -7, (7,0): -6},
                                                                                    (6,0): {(7,0): 1}, (7,0): {}})
])
def test_construction_of_h_on_dag(dists, R_set, r, expected_h):
    graph, neg_edges = load_test_case(TESTDATA_FILEPATH + "small_flow_dag.json")

    h, _, mapping = _construct_h(graph, neg_edges, dists, R_set, r)

    inv_mapping = {v:k for k,v in mapping.items()}

    assert all(inv_mapping[vertex] in expected_h for vertex in h.keys())
    assert all(len(expected_h[inv_mapping[vertex]]) == len(edges) for vertex, edges in h.items())
    assert all(expected_h[inv_mapping[vertex]][inv_mapping[neighbor]] == weight for vertex, edges in h.items() for
               neighbor, weight in edges.items())


@pytest.mark.parametrize("dists,R_set,r,expected_h", [
    ([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,-6,0,-2,0,0,-2,-5,0,0,0,-3,-4], [0,0,-6,0,-7,0,-5,-2,-11,0,-9,0,-3,-6]],
     {2,5,8,10,11}, 2,
     {  (0,0): {(1,0): 3, (2,1): 0, (3,0): 7}, (1,0): {(7,0): -2}, (2,0): {(2,1): 6, (4,0): -1, (8,1): 0},
     (2,1): {(2,2): 0, (4,0): -7, (8,2): 0}, (2,2): {(2,0): -6}, (3,0): {(4,0): -2, (5,0): 4},
     (4,0): {(6,0): 5}, (5,0): {(5,1): 0, (6,0): 5, (9,0): 9}, (5,1): {(5,2): 0, (6,0): 5, (9,0): 9},
     (5,2): {(5,0): 0, (6,0): 5, (9,0): 9}, (6,0): {(2,0): 9, (8,1): 2, (13,0): 3}, (7,0): {(8,0): 1, (11,0): 5},
     (8,0): {(8,1): 5, (10,0): 2}, (8,1): {(8,2): 6, (10,1): -3}, (8,2): {(8,0): -11, (10,2): 0},
     (9,0): {(13,0): -4}, (10,0): {(6,0): 4, (10,1): 0, (12,0): 7}, (10,1): {(6,0): 4, (10,2): 9, (12,0): 7},
     (10,2): {(6,0): -5, (10,0): -9, (12,0): -2}, (11,0): {(11,1): 0, (12,0): -3}, (11,1): {(11,2): 0, (12,0): -3},
     (11,2): {(11,0): 0}, (12,0): {(13,0): 10}, (13,0): {}
      }
    )
])
def test_construction_of_h_on_random_graph(dists, R_set, r, expected_h):
    graph, neg_edges = load_test_case(TESTDATA_FILEPATH + "graph_with_neg_edges.json")

    h, _, mapping = _construct_h(graph, neg_edges, dists, R_set, r)

    inv_mapping = {v: k for k, v in mapping.items()}

    assert all(inv_mapping[vertex] in expected_h for vertex in h.keys())
    assert all(len(expected_h[inv_mapping[vertex]]) == len(edges) for vertex, edges in h.items())
    assert all(expected_h[inv_mapping[vertex]][inv_mapping[neighbor]] == weight for vertex, edges in h.items() for
               neighbor, weight in edges.items())


@pytest.mark.parametrize("filename,r", [
    ("negative_cycle_4.json", 1),
    ("graph_with_neg_cycle.json", 2)
])
def test__elimination_by_hop_reduction_detects_negative_cycle(filename, r):
    graph, neg_edges = load_test_case(TESTDATA_FILEPATH + filename)

    with pytest.raises(NegativeCycleError):
        _elimination_by_hop_reduction(graph, neg_edges, r)


@pytest.mark.parametrize("filename,r", [
    ("graph_with_neg_edges.json", 2)
])
def test_elimination_returns_same_length_price_function_as_graphs(filename, r):
    graph, neg_edges = load_test_case(TESTDATA_FILEPATH + filename)

    distances = _elimination_by_hop_reduction(graph, neg_edges, r)

    assert len(distances) == len(graph.keys())