import glob
import os
from pathlib import Path
import numpy as np
import csv
import matplotlib.pyplot as plt
import argparse

DEFAULT_PATH = "empiric_data/"

def visualize_timings(csvfile_path: Path):
    family_times = {}
    if not os.path.isdir(Path.cwd() / "plots"):
        os.makedirs(Path.cwd() / "plots")
    
    with open(csvfile_path, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            if row['graph_family'] not in family_times:
                family_times[row['graph_family']] = {}
            
            n = int(row['vertices'])
            m = int(row['edges'])

            if row['graph_family'] == "random-no-neg-cycles-1":
                scalar = int(m/n)
                if scalar not in family_times[row['graph_family']]:
                    family_times[row['graph_family']][scalar] = []
                
                family_times[row['graph_family']][scalar].append((n, float(row['fineman_time']), float(row['bellman_ford_time'])))
            elif row['graph_family'] == "random-no-neg-cycles-2":
                scalar = int(m/n)
                if (scalar,float(row['neg_edge_ratio'])) not in family_times[row['graph_family']]:
                    family_times[row['graph_family']][(scalar,float(row['neg_edge_ratio']))] = []
                family_times[row['graph_family']][(scalar,float(row['neg_edge_ratio']))].append((n, float(row['fineman_time']), float(row['bellman_ford_time'])))
            elif row['graph_family'] == "watts-strogatz":
                print(row['neg_edge_ratio'])
                if (int(row['neighbors']),float(row['neg_edge_ratio']),float(row['probability'])) not in family_times[row['graph_family']]:
                    family_times[row['graph_family']][(int(row['neighbors']),float(row['neg_edge_ratio']),float(row['probability']))] = []
                family_times[row['graph_family']][(int(row['neighbors']),float(row['neg_edge_ratio']),float(row['probability']))].append((n, float(row['fineman_time']), float(row['bellman_ford_time'])))
            else:
                ratio = row['neg_edge_ratio']
                if ratio not in family_times[row['graph_family']]:
                    family_times[row['graph_family']][ratio] = []
                
                family_times[row['graph_family']][ratio].append((n, float(row['fineman_time']), float(row['bellman_ford_time'])))

    
    for graph_type, vmap in family_times.items():
        for ke,values in vmap.items():
            values.sort(key=lambda x: x[0])
            x_values = np.array([int(v[0]) for v in values])
            
            plt.figure(figsize=(10, 6))
            plt.xscale("log")
            plt.loglog(x_values, [float(v[1]) for v in values], 'mo-', linewidth=2, markersize=8, label='Fineman Running time')
            plt.loglog(x_values, [float(v[2]) for v in values], 'bo-', linewidth=2, markersize=8, label='Bellman-Ford Running time')

            if graph_type == 'grid':
                plt.xlabel('Size of grid (n x n)', fontsize=16)
            else:
                plt.xlabel('Number of vertices (n)', fontsize=16)

            plt.xticks(fontsize=14)
            plt.yticks(fontsize=14)
            plt.ylabel('Time (seconds)', fontsize=16)
            plt.grid(True, which="both", ls="--", alpha=0.8)
            plt.legend(fontsize=14)

            plt.tight_layout()
            if graph_type == "random-no-neg-cycles-2":
                plt.savefig(Path("plots/"+f"fineman_bford_comparison_{graph_type}_{ke[0]}_{1-float(ke[1])}-{ke[1]}.png"), transparent=True)
            elif graph_type == "watts-strogatz":
                plt.savefig(Path("plots/"+f"fineman_bford_comparison_{graph_type}_neighbors_{ke[0]}_ratios_{1-float(ke[1])}-{ke[1]}_probabilities_{ke[2]}.png"), transparent=True)
            else:
                plt.savefig(Path("plots/"+f"fineman_bford_comparison_{graph_type}_{1-float(ke)}-{ke}.png"), transparent = True)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path",nargs="?", default=DEFAULT_PATH)
    args = parser.parse_args()

    file_path = args.path
    if file_path == DEFAULT_PATH:
        csv_folders = glob.glob(f"{file_path}*")
        latest_folder = max(csv_folders, key=os.path.getctime)
        file_path = [os.path.join(latest_folder, f) for f in os.listdir(latest_folder) if "SSSP_comparison" in f][0]
        print(file_path)
    visualize_timings(file_path)

if __name__ == "__main__":
    main()

