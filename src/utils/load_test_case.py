import json
import os

def load_test_case(path: str) -> dict[int, dict[int, int]]:

    with open(path, 'r') as file:
        data = json.load(file)
    
    graph = { int(k): {neighbor : weight for neighbor, weight in v} for k, v in data.items() }

    return graph

def main():
    print(os.getcwd())

if __name__ == "__main__":
    main()