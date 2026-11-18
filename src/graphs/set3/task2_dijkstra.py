"""Set 3, task 2: shortest paths using the basic Dijkstra algorithm."""
from math import inf

from graphs.set3 import task1_connected_weighted


def init(G, s):
    """Initialize distances and predecessors; vertices are numbered from 0."""
    if not isinstance(s, int) or isinstance(s, bool) or not 0 <= s < len(G):
        raise ValueError(f"Wierzchołek startowy musi być liczbą całkowitą od 1 do {len(G)}.")
    ds = [inf] * len(G)
    ps = [None] * len(G)
    ds[s] = 0
    return ds, ps


def relax(u, v, w, ds, ps):
    """Improve the route to v through u, using canonical undirected edge keys."""
    weight = w[min(u, v), max(u, v)]
    if ds[v] > ds[u] + weight:
        ds[v] = ds[u] + weight
        ps[v] = u


def dijkstra(G, w, s):
    """Return (distances, predecessors) without modifying G or w.

    G is list[set[int]]; w maps (min(u, v), max(u, v)) to nonnegative weights.
    Unreachable vertices retain distance inf and predecessor None.
    Minimum selection scans unfinished vertices.
    """
    ds, ps = init(G, s)
    for u, neighbours in enumerate(G):
        for v in neighbours:
            key = (min(u, v), max(u, v))
            if key not in w or not 0 <= w[key] < inf:
                raise ValueError("Każda krawędź musi mieć skończoną, nieujemną wagę.")

    S = set()
    while len(S) < len(G):
        u = min((v for v in range(len(G)) if v not in S), key=lambda v: ds[v])
        if ds[u] == inf:
            break
        S.add(u)
        for v in sorted(G[u]):
            if v not in S:
                relax(u, v, w, ds, ps)
    return ds, ps


def reconstruct_path(ps, s, v):
    """Return a 0-based path, or None for an unreachable/broken predecessor chain."""
    for vertex in (s, v):
        if not isinstance(vertex, int) or isinstance(vertex, bool) or not 0 <= vertex < len(ps):
            raise ValueError("Wierzchołek nie należy do grafu.")
    path = []
    seen = set()
    while v is not None:
        if v in seen or not 0 <= v < len(ps):
            return None
        seen.add(v)
        path.append(v)
        if v == s:
            return path[::-1]
        v = ps[v]
    return None


def demo():
    """Use task 1's stored graph and print every shortest path from the source."""
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
        answer = input(f"Wierzchołek startowy s od 1 do {len(graph)} (Enter = 1): ").strip()
        try:
            s = (int(answer) if answer else 1) - 1
        except ValueError:
            raise ValueError("Wierzchołek startowy musi być liczbą całkowitą.")
        ds, ps = dijkstra(graph, weights, s)
    except ValueError as exc:
        print(f"Błąd danych: {exc}")
        return

    print(f"\nSTART: s = {s + 1}\n")
    for v, distance in enumerate(ds):
        path = reconstruct_path(ps, s, v)
        if path is None:
            print(f"d({v + 1}) = ∞  ==> brak ścieżki")
        else:
            route = " - ".join(str(u + 1) for u in path)
            print(f"d({v + 1}) = {distance}  ==> [{route}]")
