import datetime
import os

from pathlib import Path
from src.fineman.finemans_algorithm import fineman
from src.scripts.bellman_ford import *
from src.utils.cycle_error import NegativeCycleError
from src.utils import load_test_case
from src.scripts.synthetic_graph_generator import single_graph_generator
from src.scripts.random_graph_no_neg_cycles_gen import generate_random_no_neg_cycles_graph_1, \
    generate_random_no_neg_cycles_graph_2
import cProfile
import pstats
from pstats import SortKey
import numpy as np
import csv
import time
import random as rand

GRAPHS_PATH = "src/tests/test_data/synthetic_graphs/"


def load_new_graph(graph_info):
    if graph_info[0] == "grid":
        n = int(graph_info[1].split('x')[0])
    else:
        n = int(graph_info[1])
    new_path = ""

    if "watts-strogatz" in graph_info[0]:
        ratio = float((graph_info[3][0] + '.' + graph_info[3][1:]))
        k = int(graph_info[4])
        p = float((graph_info[5][0] + '.' + graph_info[5][1:]))
        new_path = single_graph_generator(graph_info[0] , int(n), (1.0-ratio, ratio), k=k, p=p)
    
    elif "random" in graph_info[0] and "tree" not in graph_info[0]:
        scalar = int(int(graph_info[2])/n)
        
        if '1' in graph_info[0]:
            new_path = generate_random_no_neg_cycles_graph_1(n, scalar)
        elif '2' in graph_info[0]:
            ratio = float((graph_info[4][0] + '.' + graph_info[4][1:]))
            new_path = generate_random_no_neg_cycles_graph_2(n, scalar, (1.0-ratio, ratio))
        else:
            ratio = float((graph_info[3][0] + '.' + graph_info[3][1:]))
            new_path = single_graph_generator(graph_info[0], int(n), (1-ratio, ratio), scalar=scalar)

    else:
        ratio = float((graph_info[3][0] + '.' + graph_info[3][1:]))
        new_path = single_graph_generator(graph_info[0], int(n), (1.0-ratio, ratio))
    
    graph,_ = load_test_case(Path(GRAPHS_PATH + new_path + ".json"))
    return graph, new_path

def time_algorithms():
    if not os.path.isdir(Path.cwd() / "empiric_data"):
        os.makedirs(Path.cwd() / "empiric_data")

    files = [filename for filename in os.listdir(GRAPHS_PATH) if "Store" not in filename]
    files = sorted(files, key=lambda x: (x.split("_")[0], int(x.split("_")[1]), int(x.split("_")[2]), x.split("_")[3]))

    dte = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    name = f"{dte}" + "_SSSP_comparison"
    os.makedirs(Path.cwd() / "empiric_data" / f"{name}")
    file_path = Path.cwd() / "empiric_data" / f"{name}" / f"{name}.csv"

    for graph_file in files:
        graph,_ = load_test_case(Path(GRAPHS_PATH + graph_file))
        file_name = os.path.basename(os.path.normpath(graph_file))

        graph_info = Path(file_name).stem.split('_')
        
        graph_file = get_graph_file_name(name, graph_info)
        print(graph_file)

        bellmanford_times = []
        fineman_times = []

        count = 0
        while count < 20:
            print(count)
            try:
                bford_graph = graph.copy()
                if rand.random() > 0.5:
                    fineman_start_time = time.time()
                    result2 = fineman(graph, 0)
                    fineman_end_time = time.time()

                    bford_start_time = time.time()
                    result1 = standard_bellman_ford(bford_graph, 0, False)
                    bford_end_time = time.time()
                else:
                    bford_start_time = time.time()
                    result1 = standard_bellman_ford(bford_graph, 0, False)
                    bford_end_time = time.time()

                    fineman_start_time = time.time()
                    result2 = fineman(graph, 0)
                    fineman_end_time = time.time()

                    assert np.allclose(result1, result2, atol=1e-9)

                graph, graph_file_name = load_new_graph(graph_info)
                graph_info = Path(graph_file_name).stem.split('_')
                count += 1
            except NegativeCycleError: 
                print(NegativeCycleError)
                graph, graph_file_name = load_new_graph(graph_info)
                graph_info = Path(graph_file_name).stem.split('_')
                continue


            bellmanford_times.append(bford_end_time-bford_start_time)
            fineman_times.append(fineman_end_time-fineman_start_time)

            save_line(graph_file, graph_info, bellmanford_times[-1], fineman_times[-1])


        bellmanford_time = np.mean(bellmanford_times[8:])
        fineman_time = np.mean(fineman_times[8:])


        save_line(file_path, graph_info, fineman_time, bellmanford_time)


def get_graph_info(graph_info):
    if graph_info[0] == "grid":
        n = int(graph_info[1].split('x')[0])
    else:
        n = int(graph_info[1])

    m = int(graph_info[2])
    
    neg_edges = np.nan
    ratio = np.nan
    neighbors = np.nan
    prob = np.nan

    if "watts" in graph_info[0]:
        ratio  = float((graph_info[3][0] + '.' + graph_info[3][1:]))
        neighbors = int(graph_info[4])
        prob = float((graph_info[5][0] + '.' + graph_info[5][1:]))

    elif "no-neg-cycle" in graph_info[0]:
        neg_edges = int(graph_info[3])
        if "-2" in graph_info[0]:
            ratio = float((graph_info[4][0] + '.' + graph_info[4][1:]))

    else:
        ratio = float((graph_info[3][0] + '.' + graph_info[3][1:]))
    
    return graph_info[0], n, m, neg_edges, ratio, neighbors, prob


def save_line(file_path, graph_info, fineman_time, bellmanford_time):
    name, n, m, neg_edges, ratio, neighbors, prob = get_graph_info(graph_info)

    line = {'file': file_path, 'graph_family': name,
                     'vertices': n, 'edges': m, 'neg_edges': neg_edges,
                     'neg_edge_ratio': ratio, 'neighbors': neighbors, 'probability': prob,
                     'bellman_ford_time': bellmanford_time, 'fineman_time': fineman_time}

    write_header = not os.path.exists(file_path)

    with open(file_path, 'a', newline='', buffering=1) as csvfile:
        fields = ['file', 'graph_family', 'vertices', 'edges', 'neg_edges', 'neg_edge_ratio', 'neighbors', 'probability', 'bellman_ford_time', 'fineman_time']
        writer = csv.DictWriter(csvfile, fieldnames=fields)

        if write_header:
            writer.writeheader()
        writer.writerow(line)


def get_graph_file_name(run, graph_info):
    name, n, m, neg_edges, ratio, neighbors, prob = get_graph_info(graph_info)

    if "watts" in name:
        ratio_str = str(ratio).replace(".", "")
        prob_str = str(prob).replace(".", "")
        filename = f"{name}_{n}_{ratio_str}_{neighbors}_{prob_str}"
    
    elif "random" in name and "tree" not in name:
        scalar = int(m/n)
        if "1" in name:
            filename = f"{name}_{n}_{scalar}"
        else:
            ratio_str = str(ratio).replace(".", "")
            filename = f"{name}_{n}_{scalar}_{ratio_str}"
    
    else:
        ratio_str = str(ratio).replace(".","")
        filename = f"{name}_{n}_{ratio_str}"

    return Path.cwd() / "empiric_data" / f"{run}" / f"{filename}.csv"


def main():
    profiler =  cProfile.Profile()
    profiler.enable()
    time_algorithms()
    profiler.disable()

    stats = pstats.Stats(profiler).sort_stats(SortKey.CUMULATIVE)
    stats.print_stats(10)
                
if __name__ == "__main__":
    main()