"""Set 1, task 2: draw a simple graph with vertices evenly spaced on a circle."""
import math

import matplotlib.pyplot as plt
import networkx as nx


def circle_positions(n, radius=1.0):
    """Vertex i at angle 90° - i*360°/n: first vertex on top, the rest clockwise."""
    return {
        i: (radius * math.cos(math.pi / 2 - 2 * math.pi * i / n),
            radius * math.sin(math.pi / 2 - 2 * math.pi * i / n))
        for i in range(n)
    }


def draw_graph(adj_list, title, node_colors=None, edge_weights=None, highlight_edges=None):
    """adj_list: list[set[int]] - the shared graph representation.
    node_colors: optional list with one matplotlib color per vertex (default: all pink).
    edge_weights: optional dict {(u, v): weight}, with u < v.
    highlight_edges: optional iterable of (u, v) pairs drawn thick and blue;
    other edges are thin and light gray when this argument is supplied."""
    G = nx.Graph()
    n = len(adj_list)

    G.add_nodes_from(range(n))
    for u in range(n):
        for v in adj_list[u]:
            if u < v:
                G.add_edge(u, v)

    pos = circle_positions(n)

    edge_colors = 'lightblue'
    edge_widths = 1.0
    if highlight_edges is not None:
        highlighted = {(min(u, v), max(u, v)) for u, v in highlight_edges}
        edge_colors = ['blue' if (u, v) in highlighted else 'lightgray' for u, v in G.edges()]
        edge_widths = [3.0 if (u, v) in highlighted else 1.0 for u, v in G.edges()]

    fig, ax = plt.subplots()
    ax.add_patch(plt.Circle((0, 0), 1.0, fill=False, linestyle=':', color='red'))
    # Labels 1..n as in the assignment PDFs (vertices are 0-based internally)
    nx.draw(G, pos, ax=ax, labels={i: i + 1 for i in range(n)}, node_color=node_colors if node_colors is not None else 'pink', node_size=600, font_size=14, edge_color=edge_colors, width=edge_widths)
    if edge_weights is not None:
        nx.draw_networkx_edge_labels(
            G, pos, ax=ax, edge_labels=edge_weights, font_size=10,
            rotate=False, bbox=dict(facecolor='white', edgecolor='none', alpha=0.85),
        )
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.3, 1.3)
    ax.set_aspect('equal')
    fig.suptitle(title, fontsize=14)
    # Non-blocking: the window stays open and the menu returns immediately
    plt.show(block=False)
    plt.pause(0.1)  # give the GUI a moment to render before returning
