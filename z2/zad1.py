# Import funkcji pomocniczych z Zestawu 1
from z1.utils import draw_graph, print_matrix


def is_and_construct_graphic(sequence: list[int]):
    """
    Sprawdza, czy sekwencja liczb jest ciągiem graficznym (Havel-Hakimi),
    oraz konstruuje macierz sąsiedztwa grafu prostego.
    Zwraca: (is_graphic: bool, adj_matrix: list[list[int]] | None)
    """
    if not sequence:
        return True, []

    n = len(sequence)

    # 1. Sprawdzenie warunków brzegowych dla grafu prostego
    if any(d < 0 or d >= n for d in sequence):
        return False, None

    # 2. Twierdzenie o uściskach dłoni: suma stopni musi być parzysta
    if sum(sequence) % 2 != 0:
        return False, None

    # Inicjalizacja pustej macierzy sąsiedztwa n x n
    adj_matrix = [[0] * n for _ in range(n)]

    # Przechowujemy pary: [aktualny_stopień, oryginalny_indeks_wierzchołka]
    vertices = [[deg, i] for i, deg in enumerate(sequence)]

    while True:
        # Sortowanie nierosnąco według aktualnego stopnia
        vertices.sort(key=lambda x: x[0], reverse=True)

        # Jeśli największy stopień wynosi 0, wszystkie krawędzie zostały dopasowane
        if vertices[0][0] == 0:
            return True, adj_matrix

        deg, u = vertices[0]

        # Jeśli stopień przekracza liczbę pozostałych dostępnych wierzchołków
        if deg >= len(vertices):
            return False, None

        # Łączymy wierzchołek u z kolejnymi 'deg' wierzchołkami o najwyższych stopniach
        for i in range(1, deg + 1):
            vertices[i][0] -= 1
            if vertices[i][0] < 0:
                return False, None

            v = vertices[i][1]
            adj_matrix[u][v] = 1
            adj_matrix[v][u] = 1

        # Wierzchołek u został w pełni obsłużony — usuwamy go z dalszych połączeń
        vertices.pop(0)


while True:
    user_input = input(
        "\nPodaj sekwencję liczb oddzielonych spacjami (Enter = przykład, 'q' = wyjście): "
    ).strip()

    # Opcja wyjścia z programu
    if user_input.lower() in ["q", "exit", "wyjscie", "wyjście"]:
        print("Koniec programu.")
        break

    if not user_input:
        # Ciąg graficzny z instrukcji Zestawu 2 (Rysunek 1(a))
        sequence = [4, 2, 2, 3, 2, 1, 4, 2, 2, 2, 2]
        print(f"Użyto ciągu z instrukcji: {' '.join(map(str, sequence))}")
    else:
        try:
            sequence = [int(x) for x in user_input.split()]
        except ValueError:
            print("Błąd: ciąg musi zawierać wyłącznie liczby całkowite!")
            continue

    is_graphic, adj_matrix = is_and_construct_graphic(sequence)

    degrees = [sum(row) for row in adj_matrix]
    print("Stopnie skonstruowanego grafu:", degrees)
    print("Stopnie zgodne z wejściem:", sorted(degrees) == sorted(sequence))

    if is_graphic:
        print("\nWynik: Podany ciąg JEST ciągiem graficznym.")
        print("\nMacierz sąsiedztwa skonstruowanego grafu:")
        print_matrix(adj_matrix)
        draw_graph(adj_matrix, title="Skonstruowany graf prosty (Zadanie 1)")
    else:
        print("\nWynik: Podany ciąg NIE JEST ciągiem graficznym.")