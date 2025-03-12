import os

from pathlib import Path
from src.fineman.finemans_algorithm import fineman
from src.scripts.bellman_ford import *
from src.utils import load_test_case
import csv
import time



GRAPHS_PATH = "src/tests/test_data/synthetic_graphs/"

def main():
    data = []
    for graph_file in os.listdir(GRAPHS_PATH):
        graph,neg_edges = load_test_case(Path(GRAPHS_PATH+graph_file))
        n = len(graph.keys())
        file_name = os.path.basename(os.path.normpath(graph_file))
        print(f"filename: {file_name}")
        print(graph)
        start_time = time.time()
        fineman(graph,neg_edges)
        end_time = time.time()
        fineman_time = start_time-end_time

        start_time = time.time()
        standard_bellman_ford(graph)
        end_time = time.time()
        bellman_ford_time = start_time-end_time

        # how to detect errors? make them both assert that they found an error for the same graphs?
        # make numbers very low to indicate error?
        data.append({'file_name':file_name,'no. vertices': n,'bellman_ford_time': bellman_ford_time,'fineman_time': fineman_time})


    with open("SSSP_comparison",'w',newline='') as csvfile:
        fields = ['file_name','bellman_ford_time','fineman_time']
        writer = csv.DictWriter(csvfile,fieldnames=fields)
        writer.write(data)
    csvfile.close()



if __name__ == "__main__":
    main()