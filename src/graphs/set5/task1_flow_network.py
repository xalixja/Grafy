"""Set 5, task 1: random flow network with a single source and a single sink.

Representation (the same as set 4): list[dict[int, int]], adj[u] = {v: c(u, v)}.
Vertex 0 is the source s, vertex n-1 is the sink t; the rest are printed as 2..n-1.
layers: list of vertex lists, layers[0] = [s], layers[1..N] = intermediate, layers[N+1] = [t].

Following the lecture definition, two vertices are joined by at most one arc
(no u -> v together with v -> u), so the random extra arcs never create such a pair.
"""
import random

import matplotlib.pyplot as plt
import networkx as nx

from graphs.set1.task1_representations import print_matrix
from graphs.set4.task1_digraphs import from_arcs, print_digraph_adj_list

MIN_CAPACITY, MAX_CAPACITY = 1, 10

# Network from the set 5 slides (N = 2): s=1, a=2, b=3, c=4, d=5, t=6. Max flow = 13.
EXAMPLE_ARCS = [
    (1, 2, 10), (1, 3, 9),            # s -> a, s -> b
    (2, 4, 5), (3, 5, 8),             # a -> c, b -> d
    (4, 6, 9), (5, 6, 7),             # c -> t, d -> t
    (5, 2, 4), (5, 4, 2), (3, 2, 6),  # extra arcs: d -> a, d -> c, b -> a
]
EXAMPLE_LAYERS = [[0], [1, 2], [3, 4], [5]]

# Network from input_5.pdf, figure 1 (N = 3): s=1, a..i = 2..10, t=11. Max flow = 19,
# Edmonds-Karp needs one flow cancellation (d -> a) on it.
INPUT5_ARCS = [
    (1, 2, 10), (1, 3, 3), (1, 4, 6),                 # s -> a, b, c
    (2, 3, 8), (2, 5, 8), (2, 6, 6),                  # a -> b, d, e
    (3, 6, 2), (3, 7, 10),                            # b -> e, f
    (4, 5, 9), (4, 7, 1),                             # c -> d, f
    (6, 5, 1), (5, 9, 5), (6, 10, 7), (7, 8, 9),      # e -> d, d -> h, e -> i, f -> g
    (9, 7, 8), (9, 8, 1),                             # h -> f, h -> g
    (8, 11, 7), (9, 11, 5), (10, 11, 7),              # g, h, i -> t
]
INPUT5_LAYERS = [[0], [1, 2, 3], [4, 5, 6], [7, 8, 9], [10]]


# ---------- base: names, example, printing ----------

def vertex_name(v, n):
    """'s' for the source, 't' for the sink, otherwise the 1-based number."""
    if v == 0:
        return "s"
    if v == n - 1:
        return "t"
    return str(v + 1)


def path_text(path, n):
    return " → ".join(vertex_name(v, n) for v in path)


def example_flow_network():
    """(adj, layers) of the network from the slides."""
    return from_arcs(6, EXAMPLE_ARCS), [list(layer) for layer in EXAMPLE_LAYERS]


def capacity_matrix(adj):
    """C[u][v] = c(u, v), 0 when there is no arc."""
    n = len(adj)
    return [[adj[u].get(v, 0) for v in range(n)] for u in range(n)]


def print_flow_network(adj, layers):
    n = len(adj)
    print(f"\nWierzchołki: {n} (s = 1, t = {n}), łuki: {sum(map(len, adj))}")
    print("Warstwy:")
    for i, layer in enumerate(layers):
        print(f"  {i}: {' '.join(vertex_name(v, n) for v in layer)}")
    print("\n--- Lista sąsiedztwa: v(c) ---")
    print_digraph_adj_list(adj, weighted=True)
    print("\n--- Macierz przepustowości ---")
    print_matrix(capacity_matrix(adj))


# ---------- random flow network ----------

def random_layers(N):
    """Vertex ids per layer: [s], N layers of 2..N vertices each, [t]."""
    if N < 2:
        raise ValueError("Liczba warstw pośrednich N musi być >= 2.")
    layers = [[0]]
    next_id = 1
    for _ in range(N):
        size = random.randint(2, N)
        layers.append(list(range(next_id, next_id + size)))
        next_id += size
    layers.append([next_id])
    return layers


def connect_layers(adj, layers):
    """Arcs layer i -> i+1: every vertex of layer i gets an outgoing arc,
    every vertex of layer i+1 gets an incoming one."""
    for current, nxt in zip(layers, layers[1:]):
        for u in current:
            adj[u][random.choice(nxt)] = 0
        for v in nxt:
            if not any(v in adj[u] for u in current):
                adj[random.choice(current)][v] = 0


def add_random_arcs(adj, count):
    """Add up to `count` arcs in any direction: no existing arc (in either direction),
    nothing into s, nothing out of t. Returns how many were added."""
    n = len(adj)
    s, t = 0, n - 1
    added = 0
    while added < count:
        # Rebuilt every time: picking u -> v must also rule out v -> u
        candidates = [
            (u, v) for u in range(n) for v in range(n)
            if u != v and u != t and v != s and v not in adj[u] and u not in adj[v]
        ]
        if not candidates:
            break
        u, v = random.choice(candidates)
        adj[u][v] = 0
        added += 1
    return added


def random_flow_network(N):
    """Returns (adj, layers): layered network + 2N random arcs, capacities in [1, 10]."""
    layers = random_layers(N)
    n = layers[-1][0] + 1
    adj = [dict() for _ in range(n)]

    connect_layers(adj, layers)
    added = add_random_arcs(adj, 2 * N)
    if added < 2 * N:
        print(f"Uwaga: dało się dodać tylko {added} z {2 * N} dodatkowych łuków.")

    for u in range(n):
        for v in adj[u]:
            adj[u][v] = random.randint(MIN_CAPACITY, MAX_CAPACITY)
    return adj, layers


# ---------- drawing ----------

def layer_positions(layers):
    """x = layer number, vertices of one layer spread vertically around y = 0."""
    pos = {}
    for x, layer in enumerate(layers):
        for j, v in enumerate(layer):
            pos[v] = (x, (len(layer) - 1) / 2 - j)
    return pos


def draw_flow_network(adj, layers, title, flow=None, source_side=None):
    """Layered drawing. Labels: c(u, v), or f(u, v)/c(u, v) when `flow` is given
    (saturated arcs red, arcs with flow blue, empty arcs grey).
    source_side: optional set of vertices (minimum cut side of s) drawn in green."""
    n = len(adj)
    layer_of = {v: i for i, layer in enumerate(layers) for v in layer}

    G = nx.DiGraph()
    G.add_nodes_from(range(n))
    for u in range(n):
        for v, c in adj[u].items():
            G.add_edge(u, v, c=c)
    pos = layer_positions(layers)

    # Arcs between neighbouring layers are straight, the rest are curved so they miss the vertices
    straight = [(u, v) for u, v in G.edges if layer_of[v] == layer_of[u] + 1]
    curved = [(u, v) for u, v in G.edges if layer_of[v] != layer_of[u] + 1]

    def label(u, v):
        c = adj[u][v]
        return f"{flow[u][v]}/{c}" if flow is not None else str(c)

    def color(u, v):
        if flow is None:
            return "steelblue"
        f, c = flow[u][v], adj[u][v]
        return "crimson" if f == c else "steelblue" if f > 0 else "lightgray"

    node_colors = ["pink"] * n
    if source_side is not None:
        node_colors = ["lightgreen" if v in source_side else "pink" for v in range(n)]

    width = 2.2 * len(layers) + 1
    height = 1.6 * max(map(len, layers)) + 2
    fig, ax = plt.subplots(figsize=(width, height))
    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=700, node_color=node_colors)
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=13,
                            labels={v: vertex_name(v, n) for v in range(n)})
    for edges, style in ((straight, "arc3,rad=0"), (curved, "arc3,rad=0.3")):
        if not edges:
            continue
        nx.draw_networkx_edges(G, pos, ax=ax, edgelist=edges, connectionstyle=style,
                               edge_color=[color(u, v) for u, v in edges],
                               arrows=True, arrowstyle="-|>", arrowsize=16, node_size=700, width=1.6)
        nx.draw_networkx_edge_labels(G, pos, ax=ax, connectionstyle=style, font_size=10,
                                     edge_labels={(u, v): label(u, v) for u, v in edges},
                                     label_pos=0.35, bbox={"fc": "white", "ec": "none", "alpha": 0.8})
    ax.axis("off")
    ax.margins(0.12)
    fig.suptitle(title, fontsize=14)
    # Non-blocking, like the rest of the project: the menu returns immediately
    plt.show(block=False)
    plt.pause(0.1)


# ---------- demo ----------

def read_N(default=2):
    text = input(f"Liczba warstw pośrednich N (>= 2, do testów <= 4; Enter = {default}): ").strip()
    return int(text) if text else default


def choose_network():
    """Asks for the slide example or a random network. Returns (adj, layers, title) or None."""
    choice = input("\nEnter = losowa sieć, 'p' = przykład ze slajdów (N = 2), "
                   "'w' = przykładowe wejście input_5 (N = 3): ").strip().lower()
    if choice == "p":
        adj, layers = example_flow_network()
        return adj, layers, "Sieć przepływowa ze slajdów (N = 2)"
    if choice == "w":
        adj = from_arcs(11, INPUT5_ARCS)
        return adj, [list(layer) for layer in INPUT5_LAYERS], "Przykładowe wejście – zestaw 5 (rys. 1, N = 3)"
    try:
        N = read_N()
        adj, layers = random_flow_network(N)
    except ValueError as e:
        print(f"Błąd: {e}")
        return None
    return adj, layers, f"Losowa sieć przepływowa (N = {N})"


def demo():
    """Random (or slide) flow network -> listing, capacity matrix, layered drawing."""
    chosen = choose_network()
    if chosen is None:
        return
    adj, layers, title = chosen
    print_flow_network(adj, layers)
    draw_flow_network(adj, layers, title)
