"""Set 6, task 1: PageRank by random walk and power iteration."""
from pathlib import Path
from random import Random, randrange

from graphs.menu import DATA_DIR
from graphs.set4.task1_digraphs import draw_digraph, from_arcs, random_digraph_gnp, read_n_p


def random_pagerank_graph(n, p):
    """Generate a G(n, p) digraph and add an outgoing arc to each sink."""
    if n < 2:
        raise ValueError("Do losowania potrzeba co najmniej dwóch wierzchołków.")
    adjacency = random_digraph_gnp(n, p)
    graph = {}
    for vertex, neighbours in enumerate(adjacency):
        if not neighbours:
            target = (vertex + randrange(1, n)) % n
            neighbours[target] = 1
        graph[str(vertex + 1)] = tuple(str(target + 1) for target in neighbours)
    return graph


def read_adjacency(path):
    """Read lines in the form 'vertex: neighbor1, neighbor2'."""
    graph = {}
    for number, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
        if not line.strip():
            continue
        vertex, separator, targets = line.partition(":")
        vertex = vertex.strip()
        if not separator or not vertex or vertex in graph:
            raise ValueError(f"Nieprawidłowa lista sąsiedztwa w wierszu {number}.")
        graph[vertex] = tuple(dict.fromkeys(targets.replace(",", " ").split()))
    missing = dict.fromkeys(v for targets in graph.values() for v in targets if v not in graph)
    graph.update(dict.fromkeys(missing, ()))
    return graph


def pagerank_walk(graph, steps=1_000_000, teleport=0.15, seed=None):
    if not graph or steps < 1 or not 0 < teleport <= 1:
        raise ValueError("Podaj niepusty graf, dodatnią liczbę kroków i 0 < d ≤ 1.")
    if not all(graph.values()):
        raise ValueError("Każdy wierzchołek musi mieć co najmniej jeden łuk wychodzący.")
    rng = Random(seed)
    vertices = tuple(graph)
    visits = dict.fromkeys(vertices, 0)
    vertex = rng.choice(vertices)
    for _ in range(steps):
        neighbours = graph[vertex]
        if rng.random() < teleport:
            vertex = rng.choice(vertices)
        else:
            vertex = rng.choice(neighbours)
        visits[vertex] += 1
    return {v: count / steps for v, count in visits.items()}


def pagerank_power(graph, teleport=0.15, tolerance=1e-12, max_iterations=1000):
    if not graph or not 0 < teleport <= 1 or tolerance <= 0 or max_iterations < 1:
        raise ValueError("Nieprawidłowy graf lub parametry iteracji PageRank.")
    if not all(graph.values()):
        raise ValueError("Każdy wierzchołek musi mieć co najmniej jeden łuk wychodzący.")
    n = len(graph)
    scores = dict.fromkeys(graph, 1 / n)
    uniform = teleport / n
    for iteration in range(1, max_iterations + 1):
        updated = dict.fromkeys(graph, uniform)
        for vertex, targets in graph.items():
            share = (1 - teleport) * scores[vertex] / len(targets)
            for target in targets:
                updated[target] += share
        if sum(abs(updated[v] - scores[v]) for v in graph) <= tolerance:
            return updated, iteration
        scores = updated
    raise ValueError("Metoda potęgowa nie osiągnęła zbieżności w limicie iteracji.")


def demo():
    answer = input("Wpisz ścieżkę pliku, 'losuj' lub naciśnij Enter (pagerank.txt): ").strip()
    try:
        if answer.lower() == "losuj":
            n, p = read_n_p(default_n=12, default_p=0.25)
            graph = random_pagerank_graph(n, p)
            print("\nLista sąsiedztwa wylosowanego digrafu")
            for vertex, neighbours in graph.items():
                print(f"{vertex}: {', '.join(neighbours)}")
        else:
            path = Path(answer) if answer else DATA_DIR / "set6" / "pagerank.txt"
            graph = read_adjacency(path)
        walk = pagerank_walk(graph, seed=6)
        power, iterations = pagerank_power(graph)
    except (OSError, ValueError) as exc:
        print(f"Błąd: {exc}")
        return

    for name, scores in (
        ("Błądzenie przypadkowe (1 000 000 kroków)", walk),
        (f"Metoda potęgowa ({iterations} iteracji)", power),
    ):
        print(f"\n{name}")
        ranking = sorted(scores, key=scores.get, reverse=True)
        for rank, vertex in enumerate(ranking, 1):
            print(f"{rank:>2}. {vertex}: {scores[vertex]:.6f}")

    differences = {v: abs(walk[v] - power[v]) for v in graph}
    print("\nRóżnice bezwzględne dla poszczególnych wierzchołków")
    for vertex, difference in differences.items():
        print(f"{vertex}: {difference:.6f}")

    indices = {vertex: i for i, vertex in enumerate(graph)}
    arcs = [(indices[vertex], indices[target]) for vertex, targets in graph.items() for target in targets]
    adjacency = from_arcs(len(graph), arcs, one_based=False)
    labels = {i: vertex for vertex, i in indices.items()}
    draw_digraph(adjacency, "Digraf wejściowy PageRank", node_labels=labels, block=True)
