"""Set 4, task 4: Johnson's algorithm (all-pairs shortest paths) + the whole set 4 pipeline."""
import heapq
import math

from graphs.set2.task3_components import component_colors
from graphs.set4.task1_digraphs import draw_digraph, print_digraph_adj_list, random_digraph_gnp, read_n_p
from graphs.set4.task2_kosaraju import is_strongly_connected, kosaraju, print_components
from graphs.set4.task3_bellman_ford import (
    assign_weights_without_negative_cycle,
    bellman_ford,
    example_weighted,
    random_weighted_strongly_connected,
)

EXPECTED_LISTING_4 = [
    [0, 6, 1, 2, -1, -1, -5],
    [10, 0, -5, -4, 4, -3, 0],
    [21, 11, 0, 7, 15, 2, 11],
    [15, 5, 0, 0, 9, 2, 5],
    [19, 9, 4, 5, 0, 0, -4],
    [19, 9, 4, 5, 13, 0, 9],
    [23, 13, 8, 9, 17, 4, 0],
]


# ---------- base ----------

def print_distance_matrix(D):
    """Listing 4 format: row = from, column = to (1-based header); unreachable = ∞."""
    cells = [["∞" if x == math.inf else str(x) for x in row] for row in D]
    width = max([len(c) for row in cells for c in row] + [2])
    print("     " + " ".join(str(j + 1).rjust(width) for j in range(len(D))))
    for i, row in enumerate(cells):
        print(f" {str(i + 1).rjust(3)} " + " ".join(c.rjust(width) for c in row))


# ---------- algorithms ----------

def add_s(adj):
    """
    Algorithm 6: G' = G + extra vertex s (index n) with arcs s -> v of weight 0 for every v.
    Returns: new list[dict] with n + 1 vertices (adj itself is not modified).
    """
    g2 = [dict(neighbours) for neighbours in adj]
    g2.append({v: 0 for v in range(len(adj))})
    return g2


def dijkstra(adj, s):
    """
    Shortest paths from s; all weights must be >= 0.
    Returns: dist list (math.inf = unreachable).
    """
    n = len(adj)
    dist = [math.inf] * n
    dist[s] = 0
    heap = [(0, s)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, w in adj[u].items():
            if d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(heap, (dist[v], v))
    return dist


def johnson(adj):
    """
    Distance matrix D[u][v] for all pairs (algorithm 5 from alg_4.pdf).
    Raises ValueError if the digraph has a negative cycle.
    """
    n = len(adj)

    # G' = G + s, Bellman-Ford from s
    g2 = add_s(adj)
    ok, h = bellman_ford(g2, n)
    if not ok:
        raise ValueError("Digraf zawiera cykl o ujemnej sumie wag.")

    # rescaled weights w_hat(u, v) = w(u, v) + h[u] - h[v] >= 0
    w_hat = [{v: w + h[u] - h[v] for v, w in adj[u].items()} for u in range(n)]

    # Dijkstra from every u, then undo the rescaling
    D = [[math.inf] * n for _ in range(n)]
    for u in range(n):
        d_hat = dijkstra(w_hat, u)
        for v in range(n):
            if d_hat[v] != math.inf:
                D[u][v] = d_hat[v] - h[u] + h[v]
    return D


# ---------- demos ----------

def demo():
    """Example (figure 2, checked against listing 4) or random weighted digraph -> distance matrix."""
    choice = input("\nEnter = digraf z instrukcji (rys. 2), 'l' = losuj: ").strip().lower()
    try:
        if choice == "l":
            n, p = read_n_p(default_n=7, default_p=0.4)
            adj = random_weighted_strongly_connected(n, p)
        else:
            adj = example_weighted()
        D = johnson(adj)
    except ValueError as e:
        print(f"Błąd: {e}")
        return

    print("\n--- Lista sąsiedztwa z wagami: wierzchołek(waga) ---")
    print_digraph_adj_list(adj, weighted=True)
    print("\n--- Macierz odległości (wiersz = skąd, kolumna = dokąd) ---")
    print_distance_matrix(D)
    if choice != "l":
        print("Zgodne z listingiem 4:", "TAK" if D == EXPECTED_LISTING_4 else "NIE")

    draw_digraph(adj, "Digraf z wagami (algorytm Johnsona)", weighted=True)


def demo_all():
    """Whole set 4 on one graph (input_4.pdf): G(n, p) -> Kosaraju -> weights -> Johnson."""
    try:
        n, p = read_n_p(default_n=7, default_p=0.4)
        adj = random_digraph_gnp(n, p)
    except ValueError as e:
        print(f"Błąd: {e}")
        return

    print("\n[1] Losowy digraf - lista sąsiedztwa:")
    print_digraph_adj_list(adj)

    comp = kosaraju(adj)
    print("\n[2] Kosaraju - silnie spójne składowe:")
    print_components(comp)
    if not is_strongly_connected(comp):
        draw_digraph(adj, "Digraf NIE jest silnie spójny", node_colors=component_colors(comp))
        print("\nDigraf nie jest silnie spójny - koniec. Uruchom ponownie albo zwiększ p.")
        return

    try:
        weighted = assign_weights_without_negative_cycle(adj)
        D = johnson(weighted)
    except ValueError as e:
        print(f"Błąd: {e}")
        return

    print("\n[3] Wagi - lista sąsiedztwa: wierzchołek(waga):")
    print_digraph_adj_list(weighted, weighted=True)
    ok, dist = bellman_ford(weighted, 0)
    print("\n[3] Bellman-Ford z wierzchołka 1:", " ".join(str(d) for d in dist))
    print("\n[4] Johnson - macierz odległości:")
    print_distance_matrix(D)

    draw_digraph(weighted, "Silnie spójny digraf z wagami", weighted=True)
