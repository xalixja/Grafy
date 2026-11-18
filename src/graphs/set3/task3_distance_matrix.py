"""Set 3, task 3: all-pairs distances using Dijkstra from each source."""
from math import inf

from graphs.set3 import task1_connected_weighted
from graphs.set3.task2_dijkstra import dijkstra


def distance_matrix(graph, weights) -> list[list[int | float]]:
    """Return D[s][v], the shortest distance from s to v (inf if unreachable).

    Uses the same graph and weights for every source without modifying either.
    """
    D = []
    for s in range(len(graph)):
        ds, _ = dijkstra(graph, weights, s)
        D.append(ds)
    return D


def print_distance_matrix(matrix):
    """Print aligned distances with 1-based row/column headers and ∞."""
    if not matrix:
        print("(pusta macierz)")
        return
    rows = [["∞" if value == inf else str(value) for value in row] for row in matrix]
    width = max(len(str(len(matrix))), max(len(value) for row in rows for value in row))
    print(" " * width + " | " + " ".join(str(v + 1).rjust(width) for v in range(len(matrix))))
    print("-" * width + "-+-" + "-" * (len(matrix) * (width + 1) - 1))
    for u, row in enumerate(rows):
        print(str(u + 1).rjust(width) + " | " + " ".join(value.rjust(width) for value in row))


def demo():
    """Print the distance matrix of task 1's stored weighted graph."""
    current = task1_connected_weighted.get_current_graph()
    if current is None:
        print("Brak bieżącego grafu. Wygeneruj graf z wagami w zadaniu 1.")
        task1_connected_weighted.demo()
        current = task1_connected_weighted.get_current_graph()
        if current is None:
            return

    graph, weights = current
    print(f"\nBieżący graf z zadania 1: {len(graph)} wierzchołków, {len(weights)} krawędzi.")
    try:
        D = distance_matrix(graph, weights)
    except ValueError as exc:
        print(f"Błąd danych: {exc}")
        return
    print("\n--- Macierz odległości ---")
    print_distance_matrix(D)
