import pytest
from fineman.preprocessing import *
from utils import load_test_case

TESTDATA_FILEPATH = "src/tests/test_data/"

# DEGREE OF ONE TESTS
def test_ensure_degree_of_one_for_tree_with_neg_root():
    graph = load_test_case(TESTDATA_FILEPATH + "tree_graph_two_layered_negative_root.json")
    assert len(graph[1]) == 2

    graph = ensure_neg_vertices_has_degree_of_one(graph)
    assert len(graph[1]) == 1

def test_ensure_same_graph_on_graph_with_no_neg_edges():
    graph = load_test_case(TESTDATA_FILEPATH + "complete_four_vertices_graph_with_no_neg_edges.json")
    new_graph = ensure_neg_vertices_has_degree_of_one(graph)

    assert graph == new_graph

def test_graph_already_adhere_to_one_degree_restriction():
    graph = load_test_case(TESTDATA_FILEPATH + "graph_already_adhere_to_one_degree_restriction.json")
    new_graph = ensure_neg_vertices_has_degree_of_one(graph)

    assert graph == new_graph




# DEGREE OF AT MOST THE THRESHOLD TESTS
@pytest.mark.parametrize("filename,threshold", [("tree_graph_two_layered_negative_root.json", 2), ("graph_already_adhere_to_one_degree_restriction.json", 2)])
def test_maxdegree_already_ensured(filename, threshold):
    graph = load_test_case(TESTDATA_FILEPATH + filename)
    new_graph = ensure_max_degree(graph, threshold)
    
    assert graph ==  new_graph


def test_complete_graph_is_doubled():
    graph = load_test_case(TESTDATA_FILEPATH + "complete_four_vertices_graph_with_no_neg_edges.json")
    threshold = 2
    graph = ensure_max_degree(graph, threshold)

    for _, v in graph.items():
        assert len(v) <= threshold
    
    assert len(graph.keys()) == 12

def test_one_split_not_enough():
    graph = load_test_case(TESTDATA_FILEPATH + "tree_graph_single_root_with_7_children.json")
    threshold = 3
    graph = ensure_max_degree(graph, threshold)

    for _, v in graph.items():
        assert len(v) <= threshold
    
    assert len(graph.keys()) == 12

def test_two_splits_required_on_both_sides():
    graph = load_test_case(TESTDATA_FILEPATH + "tree_graph_single_root_with_10_children.json")
    threshold = 3
    graph = ensure_max_degree(graph, threshold)

    for _, v in graph.items():
        assert len(v) <= threshold
    
    assert len(graph.keys()) == 17

@pytest.mark.parametrize("threshold,expected", [(50, 103), (15, 115), (10, 131)])
def test_multiple_splits_on_hundred_vertex_graph(threshold, expected):
    graph = load_test_case(TESTDATA_FILEPATH + "tree_graph_single_root_with_100_children.json")
    graph = ensure_max_degree(graph, threshold)

    for _, v in graph.items():
        assert len(v) <= threshold
    
    assert len(graph.keys()) == expected



# TESTS ON ENTIRE PREPROCESSING SEQUENCE
@pytest.mark.parametrize("filename,threshold", [
    ("small_graph_with_neg_edges.json", 2),
    ("high_in_degree_graph.json", 5)
])
def test_on_graph(filename, threshold):
    graph = load_test_case(TESTDATA_FILEPATH + filename)
    graph = preproces_graph(graph, threshold)

    for _, v in graph.items():
        assert len(v) <= threshold

        for _, weight in v:
            if weight < 0:
                assert len(v) <= 1

    transposed_graph, _ = transpose_graph(graph)
    for set in transposed_graph.values():
        assert len(set) <= threshold
