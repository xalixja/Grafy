"""Set 3, task 1: connect a random G(n, p) and assign edge weights in 1..10."""
import random

import matplotlib.pyplot as plt

from graphs.set1.task2_drawing import draw_graph
from graphs.set1.task3_random_graphs import generate_G_np
from graphs.set2.task3_components import components, is_connected

# Shared by the set's tasks; replaced only after explicit, successful generation.
_current_graph = None


def get_current_graph():
    """Return the stored (adj_list, weights), or None before task 1 is run.

    Future tasks should use this pair without regenerating or modifying it.
    """
    return _current_graph


def generate_connected_weighted_graph(n, p):
    """Return (list[set[int]], {(u, v): weight}) with 0 <= u < v < n.

    Add exactly k-1 edges between the k original components (no retries).
    This repairs G(n, p), rather than sampling G(n, p) conditioned on connectivity.
    The generator itself does not change the graph stored by the menu.
    """
    if not isinstance(n, int) or isinstance(n, bool) or n < 1:
        raise ValueError("Liczba wierzchołków n musi być liczbą całkowitą >= 1.")
    if not isinstance(p, (int, float)) or not 0 <= p <= 1:
        raise ValueError("Prawdopodobieństwo p musi należeć do przedziału [0, 1].")

    graph = generate_G_np(n, p)
    if not is_connected(graph):
        groups = {}
        for v, nr in enumerate(components(graph)):
            groups.setdefault(nr, []).append(v)
        groups = list(groups.values())
        random.shuffle(groups)
        connected = groups[0][:]
        for group in groups[1:]:
            # These endpoints are in different components, so the edge is new.
            u = random.choice(connected)
            v = random.choice(group)
            graph[u].add(v)
            graph[v].add(u)
            connected.extend(group)

    weights = {}
    for u, neighbours in enumerate(graph):
        for v in sorted(neighbours):
            if u < v:
                weights[u, v] = random.randint(1, 10)
    return graph, weights


def demo():
    """Generate and store the set's graph, print weighted edges and draw it."""
    global _current_graph

    try:
        answer = input("\nLiczba wierzchołków n >= 1 (Enter = 12): ").strip()
        try:
            n = int(answer) if answer else 12
        except ValueError:
            raise ValueError("Liczba wierzchołków n musi być liczbą całkowitą >= 1.")
        answer = input("Prawdopodobieństwo p z [0, 1] (Enter = 0.3): ").strip()
        try:
            p = float(answer) if answer else 0.3
        except ValueError:
            raise ValueError("Prawdopodobieństwo p musi być liczbą z przedziału [0, 1].")
        generated = generate_connected_weighted_graph(n, p)
    except ValueError as exc:
        print(f"Błąd danych: {exc}")
        return

    _current_graph = generated
    graph, weights = generated
    print(f"\nWierzchołki: {len(graph)}, krawędzie: {len(weights)}")
    print("Graf spójny:", "TAK" if is_connected(graph) else "NIE")
    print("\n--- Krawędzie z wagami ---")
    if not weights:
        print("(brak krawędzi)")
    for (u, v), weight in sorted(weights.items()):
        print(f"{u + 1} - {v + 1}: {weight}")

    draw_graph(graph, f"Spójny graf losowy z wagami, n = {n}, p = {p}", edge_weights=weights)
    plt.show(block=True)
