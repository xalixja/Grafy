"""Set 2, task 2: randomize a simple graph keeping vertex degrees (edge swaps ab, cd -> ad, bc)."""
import random

from graphs.set1.task1_representations import print_adj_list
from graphs.set1.task2_drawing import draw_graph
from graphs.set2.task1_graphic_sequence import EXAMPLE_SEQUENCE, is_and_construct_graphic


def randomize(adj_list, swaps, max_attempts_factor=100):
    """
    Performs `swaps` successful edge swaps (a, b), (c, d) -> (a, d), (b, c).
    Gives up after max_attempts_factor * swaps attempts (some graphs allow no swap at all).

    adj_list: list[set[int]] - not modified.
    Returns: (before, after) - copy of the input graph and the randomized graph.
    """
    before = [set(neighbours) for neighbours in adj_list]
    after = [set(neighbours) for neighbours in adj_list]

    # edges <- list of edges (u, v) with u < v, built from `after`
    edges = []
    for u, neighbours in enumerate(after):
        for v in neighbours:
            if u < v:
                edges.append((u, v))

    # fewer than 2 edges -> print a message and return before, after
    if len(edges) < 2:
        print("Graf ma mniej niż 2 krawędzie - randomizacja niemożliwa.")
        return before, after

    # Main loop: stop after `swaps` successful swaps or after max_attempts attempts
    done = 0
    attempts = 0
    max_attempts = max_attempts_factor * swaps

    while done < swaps and attempts < max_attempts:
        attempts += 1

        # two different positions in the edge list
        i, j = random.sample(range(len(edges)), 2)
        a, b = edges[i]
        c, d = edges[j]
        if random.random() < 0.5:  # reverse the second edge with probability 1/2
            c, d = d, c

        # a, b, c, d must be four different vertices
        if len({a, b, c, d}) < 4:
            continue

        # new edges ad and bc must not exist yet
        if d in after[a] or c in after[b]:
            continue

        # swap in the graph
        after[a].remove(b)
        after[b].remove(a)
        after[c].remove(d)
        after[d].remove(c)
        after[a].add(d)
        after[d].add(a)
        after[b].add(c)
        after[c].add(b)

        # swap in the edge list (same positions, stored as (smaller, larger))
        edges[i] = (min(a, d), max(a, d))
        edges[j] = (min(b, c), max(b, c))

        done += 1

    if done < swaps:
        print(f"Wykonano tylko {done} z {swaps} zamian - w tym grafie nie da się więcej.")

    return before, after


def demo():
    """Graph from a graphic sequence -> N swaps -> degrees check + drawings before/after."""
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

    try:
        swaps = int(input("Podaj liczbę randomizacji: "))
    except ValueError:
        print("Błąd: liczba randomizacji musi być liczbą całkowitą.")
        return
    if swaps < 0:
        print("Błąd: liczba randomizacji nie może być ujemna.")
        return

    before, after = randomize(graph, swaps)

    degrees_before = [len(neighbours) for neighbours in before]
    degrees_after = [len(neighbours) for neighbours in after]
    print(f"\nStopnie przed: {degrees_before}")
    print(f"Stopnie po:    {degrees_after}")
    print("Stopnie zachowane:", "TAK" if degrees_before == degrees_after else "NIE - BŁĄD!")

    print("\n--- Lista sąsiedztwa po randomizacji ---")
    print_adj_list(after)

    draw_graph(before, "Przed randomizacją")
    draw_graph(after, f"Po {swaps} randomizacjach")
