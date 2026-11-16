"""Set 4, task 1: directed graphs (digraphs) - representations and random digraphs G(n, p).

Digraph representation used in the whole set 4: list[dict[int, int]],
adj[u] = {v: weight} for every arc u -> v, vertices 0..n-1 (printed 1..n).
An unweighted digraph is the same structure with every weight = 1.
"""
import random

import matplotlib.pyplot as plt
import networkx as nx

from graphs.set1.task1_representations import print_matrix
from graphs.set1.task2_drawing import circle_positions

# Digraph from figure 1 / listing 1 of the set 4 instructions (1-based arcs)
EXAMPLE_ARCS = [
    (1, 2), (1, 3), (1, 5),
    (2, 1), (2, 3), (2, 4), (2, 5), (2, 7),
    (3, 6), (4, 2), (4, 7), (5, 7), (6, 2), (7, 6),
]


# ---------- base: building, reading, printing, drawing ----------

def from_arcs(n, arcs, one_based=True):
    """Build list[dict] from arcs (u, v) or (u, v, weight); weight defaults to 1."""
    shift = 1 if one_based else 0
    adj = [dict() for _ in range(n)]
    for arc in arcs:
        u, v = arc[0] - shift, arc[1] - shift
        adj[u][v] = arc[2] if len(arc) > 2 else 1
    return adj


def example_digraph():
    """Digraph from figure 1 of the instructions (7 vertices, strongly connected)."""
    return from_arcs(7, EXAMPLE_ARCS)


def arcs_of(adj):
    """All arcs as (u, v, weight), sorted - handy for Bellman-Ford and the incidence matrix."""
    return [(u, v, w) for u in range(len(adj)) for v, w in sorted(adj[u].items())]


def read_n_p(default_n=7, default_p=0.5):
    """Ask for n and p (Enter = default). Raises ValueError on bad input."""
    answer = input(f"Podaj liczbę wierzchołków n (Enter = {default_n}): ").strip()
    n = int(answer) if answer else default_n
    answer = input(f"Podaj prawdopodobieństwo p [0, 1] (Enter = {default_p}): ").strip()
    p = float(answer) if answer else default_p
    return n, p


def print_digraph_adj_list(adj, weighted=False):
    """Listing 1 format: '1. 2 3 5' (with weights: '1. 2(6) 3(3) 5(-1)')."""
    for u, neighbours in enumerate(adj):
        items = sorted(neighbours.items())
        text = " ".join(f"{v + 1}({w})" if weighted else str(v + 1) for v, w in items)
        print(f" {str(u + 1).rjust(3)}. {text}")


def draw_digraph(adj, title, weighted=False, node_colors=None):
    """Circle layout like set 1; arcs are curved so that u->v and v->u do not overlap."""
    n = len(adj)
    G = nx.DiGraph()
    G.add_nodes_from(range(n))
    for u in range(n):
        for v, w in adj[u].items():
            G.add_edge(u, v, weight=w)

    pos = circle_positions(n)
    style = "arc3,rad=0.12"

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.add_patch(plt.Circle((0, 0), 1.0, fill=False, linestyle=":", color="red"))
    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=600,
                           node_color=node_colors if node_colors is not None else "pink")
    nx.draw_networkx_labels(G, pos, ax=ax, labels={i: i + 1 for i in range(n)}, font_size=14)
    nx.draw_networkx_edges(G, pos, ax=ax, arrows=True, arrowstyle="-|>", arrowsize=16,
                           edge_color="steelblue", node_size=600, connectionstyle=style)
    if weighted:
        labels = {(u, v): w for u, v, w in G.edges(data="weight")}
        nx.draw_networkx_edge_labels(G, pos, ax=ax, edge_labels=labels, connectionstyle=style,
                                     font_size=10, label_pos=0.4)
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.3, 1.3)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.suptitle(title, fontsize=14)
    # Non-blocking, like the rest of the project: the menu returns immediately
    plt.show(block=False)
    plt.pause(0.1)


def random_digraph_gnp(n, p):
    """
    Random digraph G(n, p): every ORDERED pair (u, v), u != v, is an arc with probability p.
    Returns: list[dict[int, int]] with all weights = 1.
    """
    if n<0:
        raise ValueError("Liczba wierzchołków n nie może być ujemna")
    if not 0 <= p <= 1:
        raise ValueError("Prawdopodobieństwo p musi należeć do przedziału [0,1].")

    adj = [dict() for _ in range(n)]

    for u in range(n):
        for v in range(n):
            if u != v and random.random() < p:
                adj[u][v] = 1

    return adj


def to_adj_matrix(adj):
    """Adjacency matrix (listing 2): M[u][v] = 1 if there is an arc u -> v. Not symmetric in general."""
    n = len(adj)
    M = [[0]*n for _ in range(n)]
    for u in range(n):
        for v in range(n):
            if v in adj[u]:
                M[u][v] = 1

    return M


def to_inc_matrix(adj):
    """
    Incidence matrix (listing 3): one column per arc, in arcs_of(adj) order;
    -1 in the row of the tail u (arc leaves u), +1 in the row of the head v (arc enters v).
    """
    n = len(adj)
    arcs = arcs_of(adj)
    M = [[0]*len(arcs) for _ in range(n)]
    for j, (u,v, _) in enumerate(arcs):
        M[u][j] = -1
        M[v][j]=1

    return M

# ---------- demo ----------

def demo():
    """Example digraph (figure 1) or random G(n, p) -> three representations + drawing."""
    choice = input("\nEnter = digraf z instrukcji (rys. 1), 'l' = losuj G(n, p): ").strip().lower()
    try:
        if choice == "l":
            n, p = read_n_p()
            adj = random_digraph_gnp(n, p)
            title = f"Losowy digraf G(n={n}, p={p})"
        else:
            adj = example_digraph()
            title = "Digraf z instrukcji (rys. 1)"
    except ValueError as e:
        print(f"Błąd: {e}")
        return

    print(f"\nWierzchołki: {len(adj)}, łuki: {sum(map(len, adj))}")
    print("\n--- Lista sąsiedztwa ---")
    print_digraph_adj_list(adj)
    print("\n--- Macierz sąsiedztwa ---")
    print_matrix(to_adj_matrix(adj))
    print("\n--- Macierz incydencji ---")
    print_matrix(to_inc_matrix(adj))

    draw_digraph(adj, title)
