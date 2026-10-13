"""Set 2, task 1: graphic sequence check and graph construction (Havel-Hakimi)."""
from graphs.set1.task1_representations import adj_list_to_adj_matrix, print_matrix
from graphs.set1.task2_drawing import draw_graph

# Graphic sequence from the Set 2 example input (Figure 1(a))
EXAMPLE_SEQUENCE = [4, 2, 2, 3, 2, 1, 4, 2, 2, 2, 2]


def is_and_construct_graphic(sequence: list[int]):
    """
    Checks whether the sequence is graphic (Havel-Hakimi)
    and builds a simple graph realising it.
    Returns: (is_graphic: bool, adj_list: list[set[int]] | None)
    """
    if not sequence:
        return True, []

    n = len(sequence)

    # 1. Bounds for a simple graph
    if any(d < 0 or d >= n for d in sequence):
        return False, None

    # 2. Handshake lemma: degree sum must be even
    if sum(sequence) % 2 != 0:
        return False, None

    # Empty graph on n vertices
    adj_list = [set() for _ in range(n)]

    # Pairs: [current_degree, original_vertex_index]
    vertices = [[deg, i] for i, deg in enumerate(sequence)]

    while True:
        # Sort by current degree, descending
        vertices.sort(key=lambda x: x[0], reverse=True)

        # Max degree is 0 -> all edges matched
        if vertices[0][0] == 0:
            return True, adj_list

        deg, u = vertices[0]

        # Degree exceeds the number of remaining vertices
        if deg >= len(vertices):
            return False, None

        # Connect u to the next 'deg' vertices with the highest degrees
        for i in range(1, deg + 1):
            vertices[i][0] -= 1
            if vertices[i][0] < 0:
                return False, None

            v = vertices[i][1]
            adj_list[u].add(v)
            adj_list[v].add(u)

        # u is fully handled - remove it
        vertices.pop(0)


def demo():
    while True:
        user_input = input(
            "\nPodaj sekwencję liczb oddzielonych spacjami (Enter = przykład, 'q' = wyjście): "
        ).strip()

        # Leave the task (back to the set menu, or end when run directly)
        if user_input.lower() in ["q", "exit", "wyjscie", "wyjście"]:
            break

        if not user_input:
            sequence = EXAMPLE_SEQUENCE
            print(f"Użyto ciągu z instrukcji: {' '.join(map(str, sequence))}")
        else:
            try:
                sequence = [int(x) for x in user_input.split()]
            except ValueError:
                print("Błąd: ciąg musi zawierać wyłącznie liczby całkowite!")
                continue

        is_graphic, graph = is_and_construct_graphic(sequence)

        if is_graphic:
            print("\nWynik: Podany ciąg JEST ciągiem graficznym.")
            print("\nMacierz sąsiedztwa skonstruowanego grafu:")
            print_matrix(adj_list_to_adj_matrix(graph))
            draw_graph(graph, title="Skonstruowany graf prosty (Zadanie 1)")
        else:
            print("\nWynik: Podany ciąg NIE JEST ciągiem graficznym.")
