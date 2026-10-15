"""Set 2, task 4: random Euler graph and its Euler cycle (Fleury's algorithm)."""
import contextlib
import io
import random

from graphs.set1.task1_representations import print_adj_list
from graphs.set1.task2_drawing import draw_graph
from graphs.set2.task1_graphic_sequence import is_and_construct_graphic
from graphs.set2.task2_randomization import randomize
from graphs.set2.task3_components import components

# Degree sequence from the Fleury example in the lecture slides
EXAMPLE_DEGREES = [4, 4, 4, 4, 4, 2, 2]


def random_euler_graph(n=None, swaps=100, max_tries=1000):
    """
    Random Euler graph: random even degrees -> graph (task 1) -> randomization (task 2)
    -> accepted only if connected (task 3).
    n: number of vertices (>= 3); None = random from 4..12.
    Returns: (degrees, adj_list) or (None, None) if no graph was found in max_tries.
    """
    if n is None:
        n = random.randint(4, 12)
    if n < 3:
        return None, None

    for _ in range(max_tries):
        # even degrees >= 2: degree sum is even and no isolated vertex
        degrees = [random.choice(range(2, n, 2)) for _ in range(n)]

        is_graphic, graph = is_and_construct_graphic(degrees)
        if not is_graphic:
            continue

        # randomization keeps degrees, so they stay even
        # (its "only k swaps done" message is muted: small graphs like a triangle allow no swap)
        with contextlib.redirect_stdout(io.StringIO()):
            _, graph = randomize(graph, swaps)

        # Euler graph <=> connected and all degrees even
        if len(set(components(graph))) == 1:
            return degrees, graph

    return None, None


def is_bridge(adj_list, u, v):
    """Naive check: remove edge u-v on a copy and see whether u and v end up in different components."""
    graph = [set(neighbours) for neighbours in adj_list]
    graph[u].remove(v)
    graph[v].remove(u)
    comp = components(graph)
    return comp[u] != comp[v]


def fleury(adj_list, start=0):
    """
    Euler cycle in an Euler graph (Fleury's algorithm).
    Walks edges in random order, removing them, and crosses a bridge only when there is no other way.
    adj_list: list[set[int]] - not modified.
    Returns: list of visited vertices (stack), first == last.
    """
    graph = [set(neighbours) for neighbours in adj_list]
    stack = [start]
    u = start

    while graph[u]:
        neighbours = list(graph[u])
        random.shuffle(neighbours)
        v = neighbours[0]

        # With more than one edge at u, at most one of them is a bridge - take another one
        if len(neighbours) > 1 and is_bridge(graph, u, v):
            v = neighbours[1]

        graph[u].remove(v)
        graph[v].remove(u)
        stack.append(v)
        u = v

    return stack


def format_cycle(cycle):
    """[1 - 2 - 3 - 1] with 1-based vertex numbers."""
    return "[" + " - ".join(str(v + 1) for v in cycle) + "]"


def demo():
    """n (or random) -> random Euler graph -> Euler cycle + drawing."""
    answer = input("\nPodaj liczbę wierzchołków n >= 3 (Enter = losowa): ").strip()
    try:
        n = int(answer) if answer else None
    except ValueError:
        print("Błąd: n musi być liczbą całkowitą.")
        return
    if n is not None and n < 3:
        print("Błąd: graf eulerowski (prosty, bez wierzchołków izolowanych) wymaga n >= 3.")
        return

    degrees, graph = random_euler_graph(n)
    if graph is None:
        print("Nie udało się wylosować grafu eulerowskiego.")
        return

    print(f"\nn = {len(graph)} => wylosowano stopnie {' '.join(map(str, degrees))}")
    print("\n--- Lista sąsiedztwa ---")
    print_adj_list(graph)

    cycle = fleury(graph)
    edges = sum(len(neighbours) for neighbours in graph) // 2
    print(f"\nCykl Eulera: {format_cycle(cycle)}")
    ok = len(cycle) == edges + 1 and cycle[0] == cycle[-1]
    print(f"Krawędzi: {edges}, kroków cyklu: {len(cycle) - 1} -> {'OK' if ok else 'BŁĄD!'}")

    draw_graph(graph, "Losowy graf eulerowski")
