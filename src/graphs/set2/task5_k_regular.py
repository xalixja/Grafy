"""Set 2, task 5: random k-regular graph (conditions -> Havel-Hakimi -> randomization)."""
from graphs.set1.task1_representations import print_adj_list
from graphs.set1.task2_drawing import draw_graph
from graphs.set2.task1_graphic_sequence import is_and_construct_graphic
from graphs.set2.task2_randomization import randomize
import matplotlib.pyplot as plt


def check_conditions(n, k):
    """
    Step 1 from the lecture: does a k-regular graph on n vertices exist?
    Returns: None if OK, otherwise an error message (str) for the user.
    """
    if n < 1 or k < 0:
        return "n musi być >= 1, a k >= 0."
    if k >= n:
        return f"k musi być mniejsze od n (wierzchołek ma najwyżej n-1 = {n - 1} sąsiadów)."
    if (n * k) % 2 != 0:
        return "n*k musi być parzyste (suma stopni = 2 * liczba krawędzi)."


def random_k_regular(n, k, swaps=100):
    """
    Random k-regular graph on n vertices.
    Step 2: sequence [k] * n -> graph (task 1, Havel-Hakimi).
    Step 3: `swaps` randomizations (task 2) - degrees stay equal to k.

    Assumes check_conditions(n, k) returned None.
    Returns: adj_list (list[set[int]]).
    """

    sequence = [k] * n
    _, graph = is_and_construct_graphic(sequence)
    _, graph = randomize(graph, swaps)

    return graph


def demo():
    """n, k (+ number of randomizations) -> random k-regular graph -> degrees check + drawing."""
    try:
        n = int(input("\nPodaj liczbę wierzchołków n: "))
        k = int(input("Podaj stopień wierzchołków k: "))
    except ValueError:
        print("Błąd: n i k muszą być liczbami całkowitymi.")
        return

    error = check_conditions(n, k)
    if error:
        print(f"Błąd: {error}")
        return

    answer = input("Podaj liczbę randomizacji (Enter = 100): ").strip()
    try:
        swaps = int(answer) if answer else 100
    except ValueError:
        print("Błąd: liczba randomizacji musi być liczbą całkowitą.")
        return
    if swaps < 0:
        print("Błąd: liczba randomizacji nie może być ujemna.")
        return

    graph = random_k_regular(n, k, swaps)

    degrees = [len(neighbours) for neighbours in graph]
    edges = sum(degrees) // 2
    print(f"\nn = {n}, k = {k}: krawędzi {edges} (oczekiwane n*k/2 = {n * k // 2})")
    print("Wszystkie stopnie równe k:", "TAK" if all(d == k for d in degrees) else "NIE - BŁĄD!")

    print("\n--- Lista sąsiedztwa ---")
    print_adj_list(graph)

    draw_graph(graph, f"Losowy graf {k}-regularny, n = {n} (po {swaps} randomizacjach)")
    plt.show(block=True)