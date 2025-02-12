import json
import os

def load_test_case(path):

    with open(path, 'r') as file:
        data = json.load(file)
    
    graph = { int(k): set(tuple(edge) for edge in v) for k, v in data.items() }

    return graph

def main():
    print(os.getcwd())

if __name__ == "__main__":
    main()