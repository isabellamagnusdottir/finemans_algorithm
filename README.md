# Thesis

This respository contains an implementation of [Fineman's algorithm][1] developed as
part of a Master thesis project at the IT-University of Copenhagen (spring 2025).

## Authors
Isabella Magnusdóttir - imag@itu.dk

Jakob Hjalgrim - jlhj@itu.dk

## Purpose
This project was created to:
- evaluate the feasibility of implementing Fineman's algorithm,
- perform performance tests on the implementation and compare with the Bellman-Ford algorithm,
- provide a foundation for future experimental research by providing a set of tools.

## Usage
To use Fineman's algorithm, import the `fineman` module from the `fineman` package,
provide the method with a graph represented as a nested dictionary mapping as such:
`dict[int,dict[int,<type>]]`, a source vertex `s`, and optionally a weight type for
`<type>`.
The support weight types are: "int","float", and "decimal" (can also give the
actual type as parameter).


To use scripts found in `src/scripts/` please refer to our `Makefile` for commands.
Since we use `poetry`, please also install the required dependencies by either running:
`make install` or manually `poetry install`, prior to running any scripts.

It is possible to generate as suite of graphs specified in `src/scripts/synthetic_graph_generator.py`
by running `make generate-graphs <type>` where `<type>` indicates the type of the weights.



Likewise, it is possible to generate random graphs using the `src/scripts/random_graph_no_neg_cycles_gen.py`
by running `make generate-random-graphs <type>`.

It is also possible to time both algorithms on all graphs within `src/tests/test_data/synthetic_graph/`
using `make time` as well as visualize the produced execution times on plots using `make visualize`.

[1]: https://dl.acm.org/doi/abs/10.1145/3618260.3649614
