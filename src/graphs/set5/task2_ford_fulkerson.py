"""Set 5, task 2: maximum flow - Ford-Fulkerson with BFS (Edmonds-Karp).

Augmenting paths are the shortest ones (fewest arcs), found with BFS in the residual network.
flow has the same shape as adj: flow[u][v] = f(u, v) for every arc u -> v.
"""
from collections import deque

from graphs.set5.task1_flow_network import (
    choose_network,
    draw_flow_network,
    path_text,
    print_flow_network,
    vertex_name,
)


# ---------- base: residual network, BFS ----------

def residual_network(adj, flow):
    """G_f: c_f(u, v) = c(u, v) - f(u, v) for arcs of G (what can still be sent),
    c_f(v, u) = f(u, v) for opposite arcs (what can be cancelled). Only c_f > 0 is kept."""
    n = len(adj)
    cf = [dict() for _ in range(n)]
    for u in range(n):
        for v, c in adj[u].items():
            f = flow[u][v]
            if c - f > 0:
                cf[u][v] = cf[u].get(v, 0) + c - f
            if f > 0:
                cf[v][u] = cf[v].get(u, 0) + f
    return cf


def bfs_shortest_path(cf, s, t):
    """BFS in G_f from s. Returns (path s..t or None, set of vertices reached from s)."""
    parent = {s: None}
    queue = deque([s])
    while queue:
        u = queue.popleft()
        for v in sorted(cf[u]):
            if v not in parent:
                parent[v] = u
                queue.append(v)
    if t not in parent:
        return None, set(parent)

    path = [t]
    while parent[path[-1]] is not None:
        path.append(parent[path[-1]])
    return path[::-1], set(parent)


def augment(adj, flow, path, amount):
    """Lines 6-12 of the algorithm: arc of G -> increase f(u, v),
    opposite arc -> cancel flow f(v, u)."""
    for u, v in zip(path, path[1:]):
        if v in adj[u]:
            flow[u][v] += amount
        else:
            flow[v][u] -= amount


def flow_value(flow, s):
    """|f| = sum of f(s, v) (no arc enters s)."""
    return sum(flow[s].values())


# ---------- Edmonds-Karp ----------

def edmonds_karp(adj, s=0, t=None):
    """
    Returns (flow, |f_max|, steps, source_side):
    steps - list of (path, c_f(p), |f| after the step) for every augmenting path,
    source_side - vertices reachable from s in the final G_f (s side of a minimum cut).
    """
    n = len(adj)
    t = n - 1 if t is None else t
    flow = [{v: 0 for v in adj[u]} for u in range(n)]
    steps = []

    while True:
        cf = residual_network(adj, flow)
        path, reached = bfs_shortest_path(cf, s, t)
        if path is None:
            return flow, flow_value(flow, s), steps, reached
        cf_p = min(cf[u][v] for u, v in zip(path, path[1:]))
        augment(adj, flow, path, cf_p)
        steps.append((path, cf_p, flow_value(flow, s)))


# ---------- checks and printing ----------

def check_flow(adj, flow, s, t):
    """Capacity (1) and conservation (2) conditions. Returns a list of violations (empty = OK)."""
    n = len(adj)
    errors = []
    balance = [0] * n
    for u in range(n):
        for v, c in adj[u].items():
            f = flow[u][v]
            if not 0 <= f <= c:
                errors.append(f"0 ≤ f ≤ c nie zachodzi dla {vertex_name(u, n)} → {vertex_name(v, n)}: {f}/{c}")
            balance[u] -= f
            balance[v] += f
    for v in range(n):
        if v not in (s, t) and balance[v] != 0:
            errors.append(f"wierzchołek {vertex_name(v, n)}: wpływa − wypływa = {balance[v]}")
    return errors


def cut_capacity(adj, source_side):
    """c(S, T): sum of capacities of arcs leaving S."""
    return sum(c for u in source_side for v, c in adj[u].items() if v not in source_side)


def print_steps(steps, n):
    print("\n--- Ścieżki powiększające (BFS, najmniej krawędzi) ---")
    if not steps:
        print("Brak ścieżki z s do t.")
    for i, (path, cf_p, value) in enumerate(steps, start=1):
        print(f"{i}. {path_text(path, n)},  c_f(p) = {cf_p},  |f| = {value}")
    print(f"{len(steps) + 1}. BFS: brak ścieżki powiększającej w G_f → koniec.")


def print_flow(adj, flow):
    n = len(adj)
    print("\n--- Przepływ na łukach: f/c ---")
    for u in range(n):
        for v in sorted(adj[u]):
            f, c = flow[u][v], adj[u][v]
            mark = "  (nasycony)" if f == c else ""
            print(f"  {vertex_name(u, n):>2} → {vertex_name(v, n):<2}  {f:>2}/{c:<2}{mark}")


# ---------- demo ----------

def demo():
    """Network from task 1 (random or slide) -> Edmonds-Karp step by step -> drawing f/c + min cut."""
    chosen = choose_network()
    if chosen is None:
        return
    adj, layers, title = chosen
    n = len(adj)
    s, t = 0, n - 1

    print_flow_network(adj, layers)
    draw_flow_network(adj, layers, title)

    flow, value, steps, source_side = edmonds_karp(adj, s, t)
    print_steps(steps, n)
    print_flow(adj, flow)

    errors = check_flow(adj, flow, s, t)
    print("\nWarunki przepustowości i zachowania przepływu:", "OK" if not errors else "BŁĄD")
    for e in errors:
        print("  " + e)

    print(f"\nMaksymalny przepływ |f_max| = {value}")
    side = " ".join(vertex_name(v, n) for v in sorted(source_side))
    print(f"Minimalny przekrój: S = {{{side}}}, c(S, T) = {cut_capacity(adj, source_side)} (= |f_max|)")

    draw_flow_network(adj, layers, f"Maksymalny przepływ |f_max| = {value}  (f/c, zielone: S przekroju)",
                      flow=flow, source_side=source_side)
