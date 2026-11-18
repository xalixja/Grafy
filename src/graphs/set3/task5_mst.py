"""Set 3, task 5: minimum spanning tree using Kruskal and Union-Find."""
from math import isfinite

import matplotlib.pyplot as plt

from graphs.set1.task2_drawing import draw_graph
from graphs.set2.task3_components import is_connected
from graphs.set3 import task1_connected_weighted


class UnionFind:
    """Disjoint sets with path compression and union by rank."""

    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, v):
        if self.parent[v] != v:
            self.parent[v] = self.find(self.parent[v])
        return self.parent[v]

    def union(self, u, v):
        """Merge different sets and return True; return False for the same set."""
        u, v = self.find(u), self.find(v)
        if u == v:
            return False
        if self.rank[u] < self.rank[v]:
            u, v = v, u
        self.parent[v] = u
        if self.rank[u] == self.rank[v]:
            self.rank[u] += 1
        return True


def kruskal(graph, weights):
    """Return ([(u, v, weight), ...], total_weight), with 0 <= u < v < n.

    Edges are considered in (weight, u, v) order for deterministic ties.
    Does not modify graph or weights. Raises ValueError for a disconnected
    or empty graph. Time: O(n + m log m), with near-constant DSU operations.
    """
    n = len(graph)
    if n == 0:
        raise ValueError("Graf musi zawierać co najmniej jeden wierzchołek.")

    edges = []
    for u, neighbours in enumerate(graph):
        for v in neighbours:
            if u < v:
                key = (u, v)
                if key not in weights:
                    raise ValueError(f"Brak wagi krawędzi {u + 1} - {v + 1}.")
                weight = weights[key]
                if not isinstance(weight, (int, float)) or isinstance(weight, bool) or not isfinite(weight):
                    raise ValueError("Wagi krawędzi muszą być skończonymi liczbami.")
                edges.append((weight, u, v))
    edges.sort()

    sets = UnionFind(n)
    tree = []
    total = 0
    for weight, u, v in edges:
        if sets.union(u, v):
            tree.append((u, v, weight))
            total += weight
            if len(tree) == n - 1:
                break

    if len(tree) != n - 1:
        raise ValueError("Graf jest niespójny — nie istnieje drzewo rozpinające wszystkie wierzchołki.")
    return tree, total


def demo():
    """Print the MST and highlight it in the original stored weighted graph."""
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
        tree, total = kruskal(graph, weights)
    except ValueError as exc:
        print(f"Błąd danych: {exc}")
        return

    print("\n--- Minimalne drzewo rozpinające (Kruskal) ---")
    print("\nKrawędzie MST:")
    if not tree:
        print("(brak krawędzi)")
    for u, v, weight in tree:
        print(f"{u + 1} - {v + 1}  (waga: {weight})")
    print(f"\nLiczba krawędzi MST: {len(tree)}")
    print(f"Suma wag MST: {total}")
    print("Graf spójny:", "TAK" if is_connected(graph) else "NIE")
    draw_graph(
        graph, "Minimalne drzewo rozpinające — Kruskal", edge_weights=weights,
        highlight_edges={(u, v) for u, v, _ in tree},
    )
    plt.show(block=True)
