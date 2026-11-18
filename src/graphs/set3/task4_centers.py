"""Set 3, task 4: minimum distance sum and minimax centers."""
from math import isfinite

from graphs.set3 import task1_connected_weighted
from graphs.set3.task3_distance_matrix import distance_matrix


def _validate_distance_matrix(D):
    """Require a nonempty square, finite, nonnegative, symmetric distance matrix."""
    if not isinstance(D, (list, tuple)) or not D:
        raise ValueError("Macierz odległości nie może być pusta.")
    n = len(D)
    if any(not isinstance(row, (list, tuple)) or len(row) != n for row in D):
        raise ValueError("Macierz odległości musi być kwadratowa.")
    for u, row in enumerate(D):
        for v, value in enumerate(row):
            if not isinstance(value, (int, float)) or isinstance(value, bool) or not isfinite(value) or value < 0:
                raise ValueError("Odległości muszą być skończonymi, nieujemnymi liczbami; graf musi być spójny.")
        if row[u] != 0:
            raise ValueError("Na przekątnej macierzy odległości muszą być zera.")
    for u in range(n):
        for v in range(u + 1, n):
            if D[u][v] != D[v][u]:
                raise ValueError("Macierz odległości grafu nieskierowanego musi być symetryczna.")


def graph_center(D):
    """Return (0-based vertex, minimum distance sum); ties use the lowest index.

    D must be the distance matrix of a connected undirected graph.
    The matrix is not modified; shortest paths are not recomputed here.
    """
    _validate_distance_matrix(D)
    sums = [sum(row) for row in D]
    center = min(range(len(D)), key=lambda v: sums[v])
    return center, sums[center]


def minimax_center(D):
    """Return (0-based vertex, minimum eccentricity); ties use the lowest index.

    D must be the distance matrix of a connected undirected graph.
    The matrix is not modified; shortest paths are not recomputed here.
    """
    _validate_distance_matrix(D)
    eccentricities = [max(row) for row in D]
    center = min(range(len(D)), key=lambda v: eccentricities[v])
    return center, eccentricities[center]


def demo():
    """Compute both centers from one distance matrix of the stored graph."""
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
        center, total = graph_center(D)
        minimax, farthest = minimax_center(D)
    except ValueError as exc:
        print(f"Błąd danych: {exc}")
        return

    print("\n--- Centrum grafu ---")
    print(f"Centrum = {center + 1} (suma odległości: {total})")
    print("\n--- Centrum minimax ---")
    print(f"Centrum minimax = {minimax + 1} (odległość do najdalszego: {farthest})")
