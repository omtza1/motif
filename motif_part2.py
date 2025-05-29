



import networkx as nx
from itertools import combinations

def parse_graph_input(file_path):
    edges = []
    with open(file_path, "r") as f:
        for line in f:
            if line.strip():
                u, v = map(int, line.strip().split())
                edges.append((u, v))
    G = nx.DiGraph()
    G.add_edges_from(edges)
    return G

def extract_all_motifs(n):
    nodes = list(range(1, n+1))
    possible_edges = [(i, j) for i in nodes for j in nodes if i != j]
    motifs = []

    for k in range(1, len(possible_edges)+1):
        for edges in combinations(possible_edges, k):
            G = nx.DiGraph()
            G.add_nodes_from(nodes)
            G.add_edges_from(edges)
            if nx.is_weakly_connected(G):
                if not any(nx.is_isomorphic(G, M) for M in motifs):
                    motifs.append(G)
    return motifs

def count_motif_instances(input_graph, motif_size):
    motifs = extract_all_motifs(motif_size)
    counts = [0 for _ in range(len(motifs))]

    for nodes in combinations(input_graph.nodes(), motif_size):
        subgraph = input_graph.subgraph(nodes).copy()
        if not nx.is_weakly_connected(subgraph):
            continue
        for i, motif in enumerate(motifs):
            if nx.is_isomorphic(subgraph, motif):
                counts[i] += 1
                break

    with open(f"motif_instances_n_{motif_size}.txt", "w") as f:
        f.write(f"n={motif_size}\n")
        f.write(f"count={len(motifs)}\n")
        for i, motif in enumerate(motifs, 1):
            f.write(f"# {i}\n")
            f.write(f"count={counts[i-1]}\n")
            for u, v in motif.edges():
                f.write(f"{u} {v}\n")


#  'input_graph.txt' contains the input graph
input_graph = parse_graph_input("input_graph.txt")
# change n as need
n=4
count_motif_instances(input_graph, n)

