import json

def load_test_case(path):

    with open(path, 'r') as file:
        data = json.load(file)
    
    graph = { int(k): set(tuple(edge) for edge in v) for k, v in data.items() }

    return graph
