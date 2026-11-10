"""Set 4, task 2: strongly connected components (Kosaraju's algorithm)."""
from graphs.set1.task1_representations import validate_adj_matrix
from graphs.set2.task3_components import component_colors
from graphs.set4.task1_digraphs import (
    draw_digraph,
    example_digraph,
    print_digraph_adj_list,
    random_digraph_gnp,
    read_n_p,
)


# ---------- base ----------

def is_strongly_connected(comp):
    """One strongly connected component <=> the digraph is strongly connected."""
    return len(set(comp)) <= 1


def print_components(comp):
    """'nr) vertices' (1-based) + strong connectivity verdict."""
    for nr in range(1, max(comp, default=0) + 1):
        vertices = [v + 1 for v in range(len(comp)) if comp[v] == nr]
        print(f"{nr}) {' '.join(map(str, vertices))}")
    print("Digraf silnie spójny:", "TAK" if is_strongly_connected(comp) else "NIE")


def transpose(adj):
    """G^T: every arc u -> v becomes v -> u (weights kept)."""
    n = len(adj)
    gt = [dict() for _ in range(n)]
    for u, neighbours in enumerate(adj):
        for v, w in neighbours.items():
            gt[v][u] = w
    return gt


def kosaraju(adj):
    """
    Strongly connected components (algorithms 1-3 from alg_4.pdf, stack variant).
    Returns: comp - comp[v] is the number (from 1) of the component of v.
    """
    n = len(adj)
    d=[-1]*n
    f=[-1]*n
    t=0
    order=[]

    for v in adj:
        t+=1
        d[v]=t
        for u in adj[v]:
            if d[u]==-2:
                dfs_visit(u)
            t+=1
            f[v] = t
            order.append(v)

    for v in range(n):
        if d[v] == -1:
            dfs_visit(v)

    gt = transpose(adj)

    for v in gt:
        for u in gt[v]:
            if comp[u] == -1:
                comp[u] = nr
                components_r(nr, u)

    comp = [-1] * n; nr = 0
    for v in reversed(order):
        if comp[v] == -1:
            nr += 1
            comp[v] = nr
            components_r(nr, v)

    return comp


# ---------- demo ----------

def demo():
    """Example digraph or random G(n, p) -> components listing + drawing colored by component."""
    choice = input("\nEnter = digraf z instrukcji (rys. 1), 'l' = losuj G(n, p): ").strip().lower()
    try:
        if choice == "l":
            n, p = read_n_p()
            adj = random_digraph_gnp(n, p)
        else:
            adj = example_digraph()
    except ValueError as e:
        print(f"Błąd: {e}")
        return

    print("\n--- Lista sąsiedztwa ---")
    print_digraph_adj_list(adj)

    comp = kosaraju(adj)
    print("\n--- Silnie spójne składowe ---")
    print_components(comp)

    draw_digraph(adj, "Silnie spójne składowe (kolor = numer składowej)", node_colors=component_colors(comp))
