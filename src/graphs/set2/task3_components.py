"""Set 2, task 3: label connected components (DFS) and find the largest one."""
import matplotlib.pyplot as plt

from graphs.set1.task1_representations import print_adj_list
from graphs.set1.task2_drawing import draw_graph
from graphs.set2.task1_graphic_sequence import EXAMPLE_SEQUENCE, is_and_construct_graphic
from graphs.set2.task2_randomization import randomize


def components(adj_list):
    """
    Labels connected components (algorithm `components` from the instructions).
    adj_list: list[set[int]].
    Returns: comp - comp[v] is the number (from 1) of the component containing v.
    """
    nr = 0
    comp = [-1] * len(adj_list)  # -1 = not visited yet

    for v in range(len(adj_list)):
        if comp[v] == -1:
            nr += 1
            comp[v] = nr
            _components_r(nr, v, adj_list, comp)

    return comp


def _components_r(nr, v, adj_list, comp):
    """Depth-first search from v, marks every reached vertex with number nr."""
    for u in adj_list[v]:
        if comp[u] == -1:
            comp[u] = nr
            _components_r(nr, u, adj_list, comp)


def is_connected(adj_list):
    """True if the whole graph is one connected component (reused by task 4)."""
    return len(set(components(adj_list))) <= 1


def largest_component(comp):
    """Number of the component with the most vertices (the lowest number on a tie)."""
    if not comp:
        return None
    return max(range(1, max(comp) + 1), key=comp.count)


def print_components(comp):
    """Listing 'nr) vertices' (1-based) + which component is the largest."""
    for nr in range(1, max(comp, default=0) + 1):
        vertices = [v + 1 for v in range(len(comp)) if comp[v] == nr]
        print(f"{nr}) {' '.join(map(str, vertices))}")
    print(f"Najwieksza skladowa ma numer {largest_component(comp)}.")


def component_colors(comp):
    """One color per component, so the drawing matches the listing."""
    cmap = plt.get_cmap("tab20")
    return [cmap((nr - 1) % cmap.N) for nr in comp]


def demo():
    """Graph from a graphic sequence (+ optional randomization) -> components listing + colored drawing."""
    user_input = input("\nPodaj ciąg graficzny (Enter = przykład z instrukcji): ").strip()
    if not user_input:
        sequence = EXAMPLE_SEQUENCE
        print(f"Użyto ciągu z instrukcji: {' '.join(map(str, sequence))}")
    else:
        try:
            sequence = [int(x) for x in user_input.split()]
        except ValueError:
            print("Błąd: ciąg musi zawierać wyłącznie liczby całkowite!")
            return

    is_graphic, graph = is_and_construct_graphic(sequence)
    if not is_graphic:
        print("Podany ciąg NIE JEST ciągiem graficznym.")
        return

    answer = input("Podaj liczbę randomizacji (Enter = 0): ").strip()
    try:
        swaps = int(answer) if answer else 0
    except ValueError:
        print("Błąd: liczba randomizacji musi być liczbą całkowitą.")
        return
    if swaps < 0:
        print("Błąd: liczba randomizacji nie może być ujemna.")
        return
    if swaps > 0:
        _, graph = randomize(graph, swaps)

    print("\n--- Lista sąsiedztwa ---")
    print_adj_list(graph)

    comp = components(graph)
    print("\n--- Spójne składowe ---")
    print_components(comp)

    draw_graph(graph, "Spójne składowe (kolor = numer składowej)", node_colors=component_colors(comp))
