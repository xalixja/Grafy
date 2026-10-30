"""Zestaw 2, zadanie 6: sprawdzanie hamiltonowskości małych grafów."""
import matplotlib.pyplot as plt

from graphs.menu import choose_data_file
from graphs.set1.task1_representations import (
    adj_matrix_to_adj_list,
    inc_matrix_to_adj_list,
    load_rows,
    parse_adj_list,
    print_adj_list,
    rows_to_matrix,
    validate_adj_matrix,
    validate_inc_matrix,
)
from graphs.set1.task2_drawing import draw_graph
from graphs.set1.task3_random_graphs import generate_G_np
from graphs.set2.task3_components import is_connected
from graphs.set2.task4_euler import format_cycle
from graphs.set2.task5_k_regular import check_conditions, random_k_regular

# Oczekiwany przykładowy cykl: [1 - 2 - 3 - 7 - 4 - 6 - 8 - 5 - 1].
EXAMPLE_EDGES = (
    (1, 2), (1, 4), (1, 5),
    (2, 3), (2, 5), (2, 6),
    (3, 4), (3, 7),
    (4, 6), (4, 7),
    (5, 8), (6, 8), (7, 8),
)


def example_graph() -> list[set[int]]:
    graph = [set() for _ in range(8)]
    for u, v in EXAMPLE_EDGES:
        graph[u - 1].add(v - 1)
        graph[v - 1].add(u - 1)
    return graph


def find_hamilton_cycle(adj_list: list[set[int]]) -> list[int] | None:
    """Zwróć cykl Hamiltona [v0, ..., v(n-1), v0] albo None."""
    n = len(adj_list)

    # Warunki konieczne, które szybko odrzucają część przypadków.
    if n < 3 or any(len(neighbours) < 2 for neighbours in adj_list):
        return None
    if not is_connected(adj_list):
        return None

    start = 0
    path = [start]            # Stos z aktualną ścieżką.
    visited = [False] * n
    visited[start] = True

    def dfs(u: int) -> bool:
        # Jeśli odwiedziliśmy wszystkie wierzchołki, musi istnieć
        # krawędź zamykająca ścieżkę w cykl.
        if len(path) == n:
            return start in adj_list[u]

        for v in sorted(adj_list[u]):
            if not visited[v]:
                visited[v] = True
                path.append(v)

                if dfs(v):
                    return True

                # Nawrót: cofnięcie na stosie i odznaczenie wierzchołka.
                path.pop()
                visited[v] = False

        return False

    if dfs(start):
        return path + [start]
    return None


def satisfies_dirac(adj_list: list[set[int]]) -> bool:
    """Wystarczający (niekonieczny) warunek Diraca dla grafu prostego."""
    n = len(adj_list)
    return n >= 3 and all(2 * len(neighbours) >= n for neighbours in adj_list)


def load_graph_from_file() -> list[set[int]] | None:
    """Wczytaj trzy reprezentacje grafu przy użyciu parserów z zestawu 1."""
    path = choose_data_file("set2")
    if path is None:
        return None

    print("\nFormat danych:")
    print("1. Macierz sąsiedztwa")
    print("2. Macierz incydencji")
    print("3. Lista sąsiedztwa")
    representation = input("Wybierz format (1-3): ").strip()

    try:
        rows = load_rows(path)
        if representation == "1":
            matrix = rows_to_matrix(rows)
            validate_adj_matrix(matrix)
            return adj_matrix_to_adj_list(matrix)
        if representation == "2":
            matrix = rows_to_matrix(rows)
            validate_inc_matrix(matrix)
            return inc_matrix_to_adj_list(matrix)
        if representation == "3":
            return parse_adj_list(rows)

        print("Nieznany format danych.")
    except (OSError, ValueError) as exc:
        print(f"Błąd wczytywania grafu: {exc}")
    return None


def _read_int(prompt: str, *, minimum: int, default: int | None = None) -> int:
    answer = input(prompt).strip()
    value = int(answer) if answer else default
    if value is None or value < minimum:
        raise ValueError(f"Wymagana liczba całkowita >= {minimum}.")
    return value


def _random_gnp() -> list[set[int]]:
    n = _read_int("Liczba wierzchołków n >= 3 (Enter = 8): ", minimum=3, default=8)
    answer = input("Prawdopodobieństwo krawędzi p z [0, 1] (Enter = 0.4): ").strip()
    p = float(answer) if answer else 0.4
    return generate_G_np(n, p)


def _random_k_regular() -> list[set[int]]:
    n = _read_int("Liczba wierzchołków n >= 3 (Enter = 8): ", minimum=3, default=8)
    k = _read_int("Stopień wierzchołków k >= 0 (Enter = 4): ", minimum=0, default=4)
    error = check_conditions(n, k)
    if error:
        raise ValueError(error)
    return random_k_regular(n, k, swaps=100)


def demo() -> None:
    """Sprawdź graf z PDF, pliku, G(n,p) albo generatora k-regularnego."""
    print("\nWybierz graf(Enter = 1): ")
    print("1. Przykład z instrukcji")
    print("2. Wczytaj graf z pliku")
    print("3. Wylosuj graf G(n, p)")
    print("4. Wylosuj graf k-regularny")
    choice = input().strip() or "1"

    try:
        if choice == "1":
            graph = example_graph()
        elif choice == "2":
            graph = load_graph_from_file()
        elif choice == "3":
            graph = _random_gnp()
        elif choice == "4":
            graph = _random_k_regular()
        else:
            print("Nieznana opcja.")
            return
    except ValueError as exc:
        print(f"Błąd danych: {exc}")
        return

    if graph is None:
        return

    n = len(graph)
    if n > 14:
        print("To zadanie wykorzystuje przeszukiwanie wykładnicze — wybierz mały graf (maks. 14 wierzchołków).")
        return

    print(f"\nWierzchołki: {n}, krawędzie: {sum(map(len, graph)) // 2}")
    print("\n--- Lista sąsiedztwa ---")
    print_adj_list(graph)

    if satisfies_dirac(graph):
        print("\nWarunek Diraca: SPEŁNIONY (graf na pewno jest hamiltonowski).")
    else:
        print("\nWarunek Diraca: NIE SPEŁNIONY (nie rozstrzyga hamiltonowskości).")

    # Nie rozstrzygamy na podstawie samego Diraca: zawsze wykonujemy DFS.
    cycle = find_hamilton_cycle(graph)
    if cycle is None:
        print("\nGraf NIE JEST hamiltonowski - brak cyklu Hamiltona.")
    else:
        print("\nGraf JEST hamiltonowski.")
        print(f"Cykl Hamiltona: {format_cycle(cycle)}")

    draw_graph(
        graph,
        "Zadanie 6 - graf hamiltonowski"
        if cycle else "Zadanie 6 - graf niehamiltonowski"
    )

    plt.show(block=True)


if __name__ == "__main__":
    demo()
