"""Set 4, task 3: random strongly connected weighted digraph + Bellman-Ford."""
import math
import random

from graphs.set4.task1_digraphs import (
    arcs_of,
    draw_digraph,
    from_arcs,
    print_digraph_adj_list,
    random_digraph_gnp,
    read_n_p,
)
from graphs.set4.task2_kosaraju import is_strongly_connected, kosaraju

WEIGHT_RANGE = (-5, 10)
FALLBACK_RANGE = (-2, 10)
EXAMPLE_WEIGHTED_ARCS = [
    (1, 2, 6), (1, 3, 3), (1, 5, -1),
    (2, 1, 10), (2, 3, -5), (2, 4, -4), (2, 5, 4), (2, 7, 4),
    (3, 6, 2), (4, 2, 5), (4, 7, 9), (5, 7, -4), (6, 2, 9), (7, 6, 4),
]


# ---------- base ----------

def example_weighted():
    """Weighted digraph from figure 2 (no negative cycle)."""
    return from_arcs(7, EXAMPLE_WEIGHTED_ARCS)

def print_distances(dist, s):
    """Distances from s, 1-based; unreachable = ∞."""
    for v, d in enumerate(dist):
        print(f"  d({s + 1} -> {v + 1}) = {'∞' if d == math.inf else d}")

def random_weighted_strongly_connected(n, p):
    """Task 3 graph: random strongly connected digraph + weights without a negative cycle."""
    adj = random_strongly_connected(n, p)
    return assign_weights_without_negative_cycle(adj)

def random_strongly_connected(n, p, max_tries=1000):
    """Draw G(n, p) until Kosaraju finds one component. Raises ValueError after max_tries."""
    for _ in range(max_tries):
        adj = random_digraph_gnp(n, p)
        if is_strongly_connected(kosaraju(adj)): return adj
    raise ValueError("Nie udało się wylosować silnie spójnego digrafu - zwiększ p.")

def assign_random_weights(adj, low, high):
    """New digraph with the same arcs and random integer weights from [low, high]."""
    return [{v: random.randint(low, high) for v in neighbours} for neighbours in adj]

def bellman_ford(adj, s):
    """
    Shortest paths from s (algorithm 4 from alg_4.pdf); negative weights allowed.
    Returns: (ok, dist) - ok = False if a negative cycle is reachable from s.
    """
    n = len(adj)
    dist = [math.inf] * n
    dist[s] = 0
    arcs = arcs_of(adj)

    # n - 1 rounds, each relaxes every arc
    for _ in range(n - 1):
        for u, v, w in arcs:
            if dist[u] + w < dist[v]:      # relaxation
                dist[v] = dist[u] + w

    # one extra pass - any further improvement means a negative cycle
    for u, v, w in arcs:
        if dist[u] + w < dist[v]:
            return False, dist
    return True, dist


def assign_weights_without_negative_cycle(adj, tries_per_range=50):
    """
    Random weights without a negative cycle: first WEIGHT_RANGE, then FALLBACK_RANGE.
    The digraph is strongly connected, so Bellman-Ford from vertex 0 reaches every cycle.
    Returns: weighted adj. Raises ValueError if both ranges fail.
    """
    for low, high in (WEIGHT_RANGE, FALLBACK_RANGE):
        for _ in range(tries_per_range):
            weighted = assign_random_weights(adj, low, high)
            ok, _ = bellman_ford(weighted, 0)
            if ok:
                print(f"Wagi z przedziału [{low}, {high}].")
                return weighted
        if (low, high) == WEIGHT_RANGE:
            print(f"Na [{low}, {high}] ciągle ujemny cykl - przechodzę na {list(FALLBACK_RANGE)}.")
    raise ValueError("Nie udało się dobrać wag bez ujemnego cyklu.")


# ---------- demo ----------

def demo():
    """Example (figure 2) or random strongly connected weighted digraph -> Bellman-Ford from s."""
    choice = input("\nEnter = digraf z instrukcji (rys. 2), 'l' = losuj: ").strip().lower()
    try:
        if choice == "l":
            n, p = read_n_p(default_n=7, default_p=0.4)
            adj = random_weighted_strongly_connected(n, p)
        else:
            adj = example_weighted()
        answer = input(f"Wierzchołek startowy s (1..{len(adj)}, Enter = 1): ").strip()
        s = int(answer) - 1 if answer else 0
        if not 0 <= s < len(adj):
            raise ValueError(f"s musi być z przedziału 1..{len(adj)}.")
    except ValueError as e:
        print(f"Błąd: {e}")
        return

    print("\n--- Lista sąsiedztwa z wagami: wierzchołek(waga) ---")
    print_digraph_adj_list(adj, weighted=True)

    ok, dist = bellman_ford(adj, s)
    if ok:
        print(f"\n--- Bellman-Ford: odległości od wierzchołka {s + 1} ---")
        print_distances(dist, s)
    else:
        print("\nW grafie jest cykl o ujemnej sumie wag osiągalny z s - odległości nieokreślone.")

    draw_digraph(adj, "Silnie spójny digraf z wagami", weighted=True)
