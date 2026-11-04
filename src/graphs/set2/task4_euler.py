"""Set 2, task 4: random Euler graph and its Euler cycle (Fleury's algorithm)."""
import contextlib
import io
import random
import matplotlib.pyplot as plt

from graphs.set1.task1_representations import print_adj_list
from graphs.set1.task2_drawing import draw_graph
from graphs.set2.task1_graphic_sequence import is_and_construct_graphic
from graphs.set2.task2_randomization import randomize
from graphs.set2.task3_components import components, is_connected

# Degree sequence from the Fleury example in the lecture slides
EXAMPLE_DEGREES = [4, 4, 4, 4, 4, 2, 2]


# ---------- building a random Euler graph ----------

def _random_even_degrees(n):
    """n random degrees, each even and in 2..n-1.

    even -> condition from Euler's theorem
    >= 2 -> no isolated vertex (it would be a separate component)
    < n  -> possible in a simple graph
    """
    return [random.choice(range(2, n, 2)) for _ in range(n)]


def _randomize_quietly(graph, swaps):
    """Task 2 randomization without its 'only k swaps done' message
    (small graphs like a triangle allow no swap at all, which is fine here)."""
    with contextlib.redirect_stdout(io.StringIO()):
        _, randomized = randomize(graph, swaps)
    return randomized


def random_euler_graph(n=None, swaps=100, max_tries=1000):
    """
    Random Euler graph built from tasks 1-3:
      even degrees -> graph (task 1) -> randomization (task 2) -> accepted only if connected (task 3).

    n: number of vertices (>= 3); None = random from 4..12.
    Returns (degrees, adj_list), or (None, None) if nothing was found in max_tries.
    """
    if n is None:
        n = random.randint(4, 12)
    if n < 3:
        return None, None

    for _ in range(max_tries):
        degrees = _random_even_degrees(n)

        is_graphic, graph = is_and_construct_graphic(degrees)
        if not is_graphic:
            continue

        # randomization keeps every degree, so they all stay even
        graph = _randomize_quietly(graph, swaps)

        # Euler's theorem: connected + all degrees even => Euler graph
        if is_connected(graph):
            return degrees, graph

    return None, None


# ---------- Fleury's algorithm ----------

def _remove_edge(graph, u, v):
    """Undirected graph: edge u-v is stored at both ends, so remove both entries."""
    graph[u].remove(v)
    graph[v].remove(u)


def is_bridge(adj_list, u, v):
    """True if removing edge u-v disconnects u from v (naive check on a copy)."""
    graph = [set(neighbours) for neighbours in adj_list]
    _remove_edge(graph, u, v)

    comp = components(graph)
    return comp[u] != comp[v]


def fleury(adj_list, start=0):
    """
    Euler cycle in an Euler graph (Fleury's algorithm).
    Walks along edges in random order and deletes each edge it uses.
    It crosses a bridge only when there is no other edge to take.

    adj_list: list[set[int]] - not modified.
    Returns the visited vertices (stack); first == last.
    """
    graph = [set(neighbours) for neighbours in adj_list]
    stack = [start]
    u = start

    while graph[u]:  # while some edge still leaves u
        neighbours = list(graph[u])
        random.shuffle(neighbours)
        v = neighbours[0]

        # If u has more than one edge, at most one of them is a bridge, so the second one is safe
        if len(neighbours) > 1 and is_bridge(graph, u, v):
            v = neighbours[1]

        _remove_edge(graph, u, v)
        stack.append(v)
        u = v

    return stack


# ---------- presentation ----------

def format_cycle(cycle):
    """[1 - 2 - 3 - 1] with vertices numbered from 1."""
    return "[" + " - ".join(str(v + 1) for v in cycle) + "]"


def _count_edges(graph):
    """Each edge is stored twice (once at each end)."""
    return sum(len(neighbours) for neighbours in graph) // 2


def _read_n():
    """Asks for n. Enter = random. Returns (ok, n)."""
    answer = input("\nPodaj liczbę wierzchołków n >= 3 (Enter = losowa): ").strip()
    if not answer:
        return True, None

    try:
        n = int(answer)
    except ValueError:
        print("Błąd: n musi być liczbą całkowitą.")
        return False, None

    if n < 3:
        print("Błąd: graf eulerowski (prosty, bez wierzchołków izolowanych) wymaga n >= 3.")
        return False, None
    return True, n


def demo():
    """n (or random) -> random Euler graph -> Euler cycle + drawing."""
    ok, n = _read_n()
    if not ok:
        return

    degrees, graph = random_euler_graph(n)
    if graph is None:
        print("Nie udało się wylosować grafu eulerowskiego.")
        return

    print(f"\nn = {len(graph)} => wylosowano stopnie {' '.join(map(str, degrees))}")
    print("\n--- Lista sąsiedztwa ---")
    print_adj_list(graph)

    cycle = fleury(graph)
    edges = _count_edges(graph)
    print(f"\nCykl Eulera: {format_cycle(cycle)}")

    # An Euler cycle uses every edge once: m edges -> m + 1 positions, back at the start
    is_valid = len(cycle) == edges + 1 and cycle[0] == cycle[-1]
    print(f"Krawędzi: {edges}, kroków cyklu: {len(cycle) - 1} -> {'OK' if is_valid else 'BŁĄD!'}")

    draw_graph(graph, "Losowy graf eulerowski")
    plt.show(block=True)