"""Set 2, task 3: label connected components (DFS) and find the largest one."""
from collections import Counter

import matplotlib.pyplot as plt

from graphs.set1.task1_representations import print_adj_list
from graphs.set1.task2_drawing import draw_graph
from graphs.set2.task1_graphic_sequence import EXAMPLE_SEQUENCE, is_and_construct_graphic
from graphs.set2.task2_randomization import randomize

NOT_VISITED = -1


def components(adj_list):
    """
    Labels connected components (algorithm `components` from the instructions).

    adj_list: list[set[int]]
    Returns comp, where comp[v] is the number (from 1) of the component containing v.
    """
    comp = [NOT_VISITED] * len(adj_list)
    nr = 0

    for v in range(len(adj_list)):
        if comp[v] == NOT_VISITED:
            # v was not reached from any earlier vertex -> it starts a new component
            nr += 1
            comp[v] = nr
            _components_r(nr, v, adj_list, comp)

    return comp


def _components_r(nr, v, adj_list, comp):
    """Depth-first search: give number nr to every vertex reachable from v."""
    for u in adj_list[v]:
        if comp[u] == NOT_VISITED:
            comp[u] = nr
            _components_r(nr, u, adj_list, comp)


def is_connected(adj_list):
    """True if the whole graph is a single component (used by task 4)."""
    number_of_components = max(components(adj_list), default=0)
    return number_of_components <= 1


def largest_component(comp):
    """Number of the component with the most vertices (the lowest number on a tie)."""
    if not comp:
        return None

    sizes = Counter(comp)  # {component number: how many vertices it has}
    # max() keeps the first of equal values, and sorted() puts the lowest number first
    return max(sorted(sizes), key=lambda nr: sizes[nr])


def print_components(comp):
    """Prints 'nr) vertices' (vertices numbered from 1) and the largest component."""
    number_of_components = max(comp, default=0)

    for nr in range(1, number_of_components + 1):
        vertices = [v + 1 for v, v_nr in enumerate(comp) if v_nr == nr]
        print(f"{nr}) {' '.join(map(str, vertices))}")

    print(f"Najwieksza skladowa ma numer {largest_component(comp)}.")


def component_colors(comp):
    """One color per component, so the drawing matches the printed list."""
    palette = plt.get_cmap("tab20")
    return [palette((nr - 1) % palette.N) for nr in comp]


def _read_sequence():
    """Asks for a degree sequence. Enter = example from the instructions. None on bad input."""
    answer = input("\nPodaj ciąg graficzny (Enter = przykład z instrukcji): ").strip()
    if not answer:
        print(f"Użyto ciągu z instrukcji: {' '.join(map(str, EXAMPLE_SEQUENCE))}")
        return EXAMPLE_SEQUENCE

    try:
        return [int(x) for x in answer.split()]
    except ValueError:
        print("Błąd: ciąg musi zawierać wyłącznie liczby całkowite!")
        return None


def _read_swaps():
    """Asks for the number of randomizations. Enter = 0. None on bad input."""
    answer = input("Podaj liczbę randomizacji (Enter = 0): ").strip()
    if not answer:
        return 0

    try:
        swaps = int(answer)
    except ValueError:
        print("Błąd: liczba randomizacji musi być liczbą całkowitą.")
        return None

    if swaps < 0:
        print("Błąd: liczba randomizacji nie może być ujemna.")
        return None
    return swaps


def demo():
    """Graphic sequence -> graph (+ optional randomization) -> components listing + colored drawing."""
    sequence = _read_sequence()
    if sequence is None:
        return

    is_graphic, graph = is_and_construct_graphic(sequence)
    if not is_graphic:
        print("Podany ciąg NIE JEST ciągiem graficznym.")
        return

    swaps = _read_swaps()
    if swaps is None:
        return
    if swaps > 0:
        _, graph = randomize(graph, swaps)

    print("\n--- Lista sąsiedztwa ---")
    print_adj_list(graph)

    comp = components(graph)
    print("\n--- Spójne składowe ---")
    print_components(comp)

    draw_graph(graph, "Spójne składowe (kolor = numer składowej)", node_colors=component_colors(comp))
    plt.show(block=True)