.PHONY: test install clean

test:
	poetry run pytest

install:
	poetry install

build:
	poetry build

generate-graphs:
	poetry run python -m src.scripts.synthetic_graph_generator

generate-random_graphs:
	poetry run python -m src.scripts.random_graph_no_neg_cycles_gen

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	rm -rf dist
	rm -rf build