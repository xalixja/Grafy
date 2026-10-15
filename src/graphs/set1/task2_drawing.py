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


def draw_graph(adj_list, title, node_colors=None):
    """adj_list: list[set[int]] - the shared graph representation.
    node_colors: optional list with one matplotlib color per vertex (default: all pink)."""
    G = nx.Graph()
    n = len(adj_list)

    G.add_nodes_from(range(n))
    for u in range(n):
        for v in adj_list[u]:
            if u < v:
                G.add_edge(u, v)

    pos = circle_positions(n)

    fig, ax = plt.subplots()
    ax.add_patch(plt.Circle((0, 0), 1.0, fill=False, linestyle=':', color='red'))
    # Labels 1..n as in the assignment PDFs (vertices are 0-based internally)
    nx.draw(G, pos, ax=ax, labels={i: i + 1 for i in range(n)}, node_color=node_colors if node_colors is not None else 'pink', node_size=600, font_size=14, edge_color='lightblue')
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.3, 1.3)
    ax.set_aspect('equal')
    fig.suptitle(title, fontsize=14)
    # Non-blocking: the window stays open and the menu returns immediately
    plt.show(block=False)
    plt.pause(0.1)  # give the GUI a moment to render before returning
