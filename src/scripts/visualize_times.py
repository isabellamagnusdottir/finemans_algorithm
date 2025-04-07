import glob
import os
from pathlib import Path
import numpy as np
import csv
import matplotlib.pyplot as plt
import argparse

DEFAULT_PATH = "empiric_data/"

def visualize_timings(csvfile_path:Path):
    family_times = {}
    if not os.path.isdir(Path.cwd() / "plots"):
        os.makedirs(Path.cwd() / "plots")
    with open(csvfile_path, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['graph_family'] not in family_times:
                family_times[row['graph_family']] = {}
            if row['graph_family'] == "random-no-neg-cycles-1":
                n = int(row['n'])
                m = int(row['m'])
                scalar = m/n
                if scalar not in family_times[row['graph_family']]: family_times[row['graph_family']][scalar] = []
                family_times[row['graph_family']][scalar].append((int(row['n']),float(row['fineman_time']),float(row['bellman_ford_time'])))
            else:
                k = row['k']
                if k not in family_times[row['graph_family']]: family_times[row['graph_family']][k] = []
                family_times[row['graph_family']][k].append((int(row['n']),float(row['fineman_time']),float(row['bellman_ford_time'])))
    for key,vmap in family_times.items():
        for v in vmap.values():
            v = sorted(v, key=lambda x: x[0])

    
    for graph_type,vmap in family_times.items():
        for key,values in vmap.items():
            x_values = np.array([int(v[0]) for v in values])

            plt.figure(figsize=(10, 6))
            plt.xscale("log")
            plt.loglog(x_values, [float(v[1]) for v in values], 'mo-', linewidth=2, markersize=8, label='Fineman Running time')
            plt.loglog(x_values, [float(v[2]) for v in values], 'bo-', linewidth=2, markersize=8, label='Bellman-Ford Running time')

            # Add labels and title
            if graph_type == 'grid':
                plt.xlabel('Size of grid (n x n)', fontsize=14)
            else:
                plt.xlabel('Number of vertices (n)', fontsize=14)
                
            if graph_type == "random-no-neg-cycles-1":
                plt.title(f'Fineman running time - Type: {graph_type}\n with edge scalar {key}]', fontsize=14)
            elif graph_type == "random-no-neg-cycles-2":
                plt.title(f'Fineman running time - Type: {graph_type}\n with initial positive/negative edge distribution [{1-float(key)},{key}]]', fontsize=14)
            else:
                plt.title(f'Fineman running time - Type: {graph_type}\n positive/negative edge distribution: [{1-float(key)},{key}]', fontsize=14)

            plt.ylabel('Time (seconds)', fontsize=14)
            plt.grid(True, which="both", ls="--", alpha=0.8)
            plt.legend(fontsize=12)

            plt.tight_layout()
            
            plt.savefig(Path("plots/"+f"fineman_bford_comparison_{graph_type}_{1-float(key)}-{key}.png"))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path",nargs="?", default=DEFAULT_PATH)
    args = parser.parse_args()

    file_path = args.path
    if file_path == DEFAULT_PATH:
        csv_files = glob.glob(f"{file_path}*.csv")
        latest_file = max(csv_files, key=os.path.getctime)
        file_path = latest_file
    visualize_timings(file_path)

if __name__ == "__main__":
    main()

