import json
import os


def load_test_case(path: str) -> tuple[dict[int, dict[int, int]], set[tuple[int, int]]]:

    with open(path, 'r') as file:
        data = json.load(file)

    graph = {}
    neg_set = set()

    for k, v in data.items():
        vertex = int(k)
        if vertex not in graph:
            graph[vertex] = {}

        for neighbor, weight in v:
            graph[vertex][neighbor] = weight

            if weight < 0:
                neg_set.add((vertex, neighbor))

    return graph, neg_set

def main():
    print(os.getcwd())

if __name__ == "__main__":
    main()