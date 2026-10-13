"""Set 1, task 3: random graphs G(n, p) and G(n, l). Both return list[set[int]]."""
import random
from itertools import combinations

from graphs.set1.task1_representations import adj_list_to_adj_matrix, print_matrix
from graphs.set1.task2_drawing import draw_graph


# Random graph G(n, p)
def generate_G_np(n, p):
    if n < 0:
        raise ValueError("Liczba wierzchołków n nie może być ujemna.")
    if not 0 <= p <= 1:
        raise ValueError("Prawdopodobieństwo p musi należeć do przedziału [0, 1].")

    adj_list = [set() for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if random.random() < p:
                adj_list[i].add(j)
                adj_list[j].add(i)
    return adj_list


# Random graph G(n, l)
def generate_G_nl(n, l):
    if n < 0:
        raise ValueError("Liczba wierzchołków n nie może być ujemna.")
    max_edges = n * (n-1) // 2
    if not 0 <= l <= max_edges:
        raise ValueError(f"Dla {n} wierzchołków liczba krawędzi musi wynosić od 0 do {max_edges}.")

    adj_list = [set() for _ in range(n)]

    all_edges = list(combinations(range(n), 2))
    random_edges = random.sample(all_edges, l)

    for i, j in random_edges:
        adj_list[i].add(j)
        adj_list[j].add(i)

    return adj_list


def demo_gnp():
    """Task 3a: generate and draw G(n, p)."""
    try:
        n = int(input("Podaj liczbę wierzchołków (n): "))
        p = float(input("Podaj prawdopodobieństwo (p) [0.0 - 1.0]: "))
    except ValueError:
        print("Błąd: Wprowadzono niepoprawne dane. Użyj liczb.")
        return

    try:
        graph = generate_G_np(n, p)
    except ValueError as e:
        print(f"Błąd: {e}")
        return

    print("\n--- Macierz sąsiedztwa G(n, p) ---")
    print_matrix(adj_list_to_adj_matrix(graph))
    draw_graph(graph, f"Wizualizacja G(n={n}, p={p})")


def demo_gnl():
    """Task 3b: generate and draw G(n, l)."""
    try:
        n = int(input("Podaj liczbę wierzchołków (n): "))
        l = int(input("Podaj liczbę krawędzi (l): "))
    except ValueError:
        print("Błąd: Wprowadzono niepoprawne dane. Użyj liczb całkowitych.")
        return

    try:
        graph = generate_G_nl(n, l)
    except ValueError as e:
        print(f"Błąd: {e}")
        return

    print("\n--- Macierz sąsiedztwa G(n, l) ---")
    print_matrix(adj_list_to_adj_matrix(graph))
    draw_graph(graph, f"Wizualizacja G(n={n}, l={l})")
