import networkx as nx
from itertools import combinations
import os
import time

def generate_all_connected_subgraphs(n):
    output_dir = "motifs_output"
    os.makedirs(output_dir, exist_ok=True)

    start_time = time.time()

    nodes = list(range(1, n+1))
    possible_edges = [(i, j) for i in nodes for j in nodes if i != j]

    count = 0
    motifs = []

    for k in range(1, len(possible_edges)+1):
        for edges in combinations(possible_edges, k):
            G = nx.DiGraph()
            G.add_nodes_from(nodes)
            G.add_edges_from(edges)

            # Check if the graph is weakly connected
            if nx.is_weakly_connected(G):
                # Check if isomorphic to existing motif
                if not any(nx.is_isomorphic(G, M) for M in motifs):
                    motifs.append(G)
                    count += 1

    elapsed_time = time.time() - start_time
    elapsed_str = f"{elapsed_time:.5f} seconds"

    filename = os.path.join(output_dir, f"motifs_n_{n}.txt")
    with open(filename, "w") as f:
        f.write(f"n={n}\n")
        f.write(f"count={count}\n")
        for idx, G in enumerate(motifs, 1):
            f.write(f"# {idx}\n")
            for u, v in G.edges():
                f.write(f"{u} {v}\n")

    print(f"n={n}: {count} motifs found in {elapsed_str}")
    with open("timing_log.txt", "a") as log:
        log.write(f"n={n}: {count} motifs found in {elapsed_str}\n")

with open("timing_log.txt", "w") as log:
    log.write("Timing results for motif generation:\n")

##### choose n
for i in range(1, 5):
    generate_all_connected_subgraphs(i)

