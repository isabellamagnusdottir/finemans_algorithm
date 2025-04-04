import pytest
from src.fineman import rand_is
from src.utils.load_test_case import load_test_case

TESTDATA_FILEPATH = "src/tests/test_data/graphs/"

@pytest.mark.parametrize("repeat", range(10))  # Repeat 10 times
@pytest.mark.parametrize("subset,expected",[
    ({0},({0}))
])
def test_random_independent_set_for_large_weight_cycle(subset,expected,repeat):
    graph,neg_edges = load_test_case(TESTDATA_FILEPATH+"6_cycle_large_positive_weights.json")
    actual = rand_is(graph,neg_edges,subset,1)
    assert actual == expected
