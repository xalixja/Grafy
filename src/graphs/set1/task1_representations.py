"""Set 1, task 1: adjacency matrix / incidence matrix / adjacency list and conversions.

Graph representation shared by all sets: adjacency list as list[set[int]],
vertices 0..n-1 (adj[u] = set of neighbours of u). Matrices are only used for input/output.
"""
from graphs.menu import choose_data_file
from graphs.set1.task2_drawing import draw_graph


# Read rows of whitespace-separated tokens from a file (blank lines are skipped)
def load_rows(filename):
    with open(filename, 'r') as file:
        return [line.split() for line in file if line.strip()]


# Rows of tokens -> matrix of ints
def rows_to_matrix(rows):
    try:
        return [[int(x) for x in row] for row in rows]
    except ValueError:
        raise ValueError("Macierz może zawierać wyłącznie liczby całkowite.")


# Output numbers vertices from 1 (as in the assignment PDFs); internally vertices are 0-based.

# Print a matrix row by row, rows labelled 1..n
def print_matrix(matrix):
    for i, row in enumerate(matrix):
        print(f" {str(i + 1).rjust(3)} | {row}")


# Print an adjacency list in the assignment format: "1. 2 5 6"
def print_adj_list(adj_list):
    for u, neighbours in enumerate(adj_list):
        print(f" {str(u + 1).rjust(3)}. {' '.join(str(v + 1) for v in sorted(neighbours))}")


# --- Validation (simple graphs only) ---

def validate_adj_matrix(adj_matrix):
    n = len(adj_matrix)
    if n == 0:
        raise ValueError("Plik jest pusty.")
    for i, row in enumerate(adj_matrix):
        if len(row) != n:
            raise ValueError(f"Macierz sąsiedztwa musi być kwadratowa ({n}x{n}), wiersz {i + 1} ma {len(row)} elementów.")
        if any(x not in (0, 1) for x in row):
            raise ValueError(f"Macierz sąsiedztwa może zawierać tylko 0 i 1 (wiersz {i + 1}).")
        if row[i] != 0:
            raise ValueError(f"Pętla w wierzchołku {i + 1} - to nie jest graf prosty.")
        for j in range(n):
            if row[j] != adj_matrix[j][i]:
                raise ValueError(f"Macierz sąsiedztwa nie jest symetryczna (pozycje [{i + 1}][{j + 1}] i [{j + 1}][{i + 1}]).")


def validate_inc_matrix(inc_matrix):
    n = len(inc_matrix)
    if n == 0:
        raise ValueError("Plik jest pusty.")
    k = len(inc_matrix[0])
    for i, row in enumerate(inc_matrix):
        if len(row) != k:
            raise ValueError(f"Wszystkie wiersze macierzy incydencji muszą mieć {k} kolumn (wiersz {i + 1} ma {len(row)}).")
        if any(x not in (0, 1) for x in row):
            raise ValueError(f"Macierz incydencji może zawierać tylko 0 i 1 (wiersz {i + 1}).")
    edges = set()
    for col in range(k):
        ends = [u for u in range(n) if inc_matrix[u][col] == 1]
        if len(ends) != 2:
            raise ValueError(f"Kolumna {col + 1} macierzy incydencji ma {len(ends)} jedynek zamiast 2.")
        if tuple(ends) in edges:
            raise ValueError(f"Krawędź {ends[0] + 1}-{ends[1] + 1} występuje wielokrotnie - to nie jest graf prosty.")
        edges.add(tuple(ends))


def parse_adj_list(rows):
    """Rows 'label neighbour neighbour ...'. Label may end with '.', ')' or ':' (e.g. '1. 2 5 6').
    Numbering base (0 or 1) is detected from the smallest label; missing rows = isolated vertices."""
    if not rows:
        raise ValueError("Plik jest pusty.")
    try:
        parsed = [(int(row[0].rstrip('.):')), [int(x) for x in row[1:]]) for row in rows]
    except ValueError:
        raise ValueError("Lista sąsiedztwa: każdy wiersz to 'wierzchołek sąsiad sąsiad ...' (liczby całkowite).")

    base = min(label for label, _ in parsed)
    if base not in (0, 1):
        raise ValueError("Numeracja wierzchołków musi zaczynać się od 0 albo od 1.")
    n = max(max([label] + neighbours) for label, neighbours in parsed) - base + 1

    adj_list = [set() for _ in range(n)]
    seen = set()
    for label, neighbours in parsed:
        u = label - base
        if u in seen:
            raise ValueError(f"Wierzchołek {label} występuje w liście więcej niż raz.")
        seen.add(u)
        for x in neighbours:
            v = x - base
            if v < 0:
                raise ValueError(f"Niepoprawny numer sąsiada {x} (wierzchołek {label}).")
            if v == u:
                raise ValueError(f"Pętla w wierzchołku {label} - to nie jest graf prosty.")
            if v in adj_list[u]:
                raise ValueError(f"Sąsiad {x} powtórzony u wierzchołka {label} - to nie jest graf prosty.")
            adj_list[u].add(v)

    # Undirected graph: every edge must be listed at both of its ends
    for u in range(n):
        for v in adj_list[u]:
            if u not in adj_list[v]:
                raise ValueError(f"Lista niesymetryczna: {u + base} ma sąsiada {v + base}, ale {v + base} nie ma {u + base}.")
    return adj_list


# --- Conversions ---

# Adjacency matrix -> adjacency list
def adj_matrix_to_adj_list(adj_matrix):
    n = len(adj_matrix)
    adj_list = [set() for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if adj_matrix[i][j]:
                adj_list[i].add(j)
    return adj_list


# Adjacency list -> incidence matrix
def adj_list_to_inc_matrix(adj_list):
    n = len(adj_list)
    edges = set()

    for u in range(n):
        for v in adj_list[u]:
            edges.add((min(u, v), max(u, v)))

    edges = sorted(edges)
    k = len(edges)
    inc_matrix = [[0]*k for _ in range(n)]

    for i, (u, v) in enumerate(edges):
        inc_matrix[u][i] = 1
        inc_matrix[v][i] = 1

    return inc_matrix


# Incidence matrix -> adjacency matrix
def inc_matrix_to_adj_matrix(inc_matrix):
    n = len(inc_matrix)
    k = len(inc_matrix[0]) if n else 0
    adj_matrix = [[0] * n for _ in range(n)]

    for i in range(k):
        vertices = []
        for u in range(n):
            if inc_matrix[u][i] == 1:
                vertices.append(u)

        if len(vertices) == 2:
            u, v = vertices
            adj_matrix[u][v] = 1
            adj_matrix[v][u] = 1

    return adj_matrix


# Incidence matrix -> adjacency list
def inc_matrix_to_adj_list(inc_matrix):
    adj_matrix = inc_matrix_to_adj_matrix(inc_matrix)
    return adj_matrix_to_adj_list(adj_matrix)


# Adjacency matrix -> incidence matrix
def adj_matrix_to_inc_matrix(adj_matrix):
    adj_list = adj_matrix_to_adj_list(adj_matrix)
    return adj_list_to_inc_matrix(adj_list)


# Adjacency list -> adjacency matrix
def adj_list_to_adj_matrix(adj_list):
    n = len(adj_list)
    adj_matrix = [[0] * n for _ in range(n)]
    for u in range(n):
        for v in adj_list[u]:
            adj_matrix[u][v] = 1
            adj_matrix[v][u] = 1
    return adj_matrix


def demo():
    """Tasks 1 + 2: load a graph from file, print the other representations, draw it."""
    filename = choose_data_file("set1")
    if filename is None:
        return

    print("\nJaki format danych znajduje się w pliku?")
    print("1. Macierz sąsiedztwa")
    print("2. Macierz incydencji")
    print("3. Lista sąsiedztwa")
    representation = input("Wybierz format (1-3): ").strip()

    try:
        rows = load_rows(filename)
        if representation == '1':
            adj_matrix = rows_to_matrix(rows)
            validate_adj_matrix(adj_matrix)
            adj_list = adj_matrix_to_adj_list(adj_matrix)
            inc_matrix = adj_matrix_to_inc_matrix(adj_matrix)
        elif representation == '2':
            inc_matrix = rows_to_matrix(rows)
            validate_inc_matrix(inc_matrix)
            adj_matrix = inc_matrix_to_adj_matrix(inc_matrix)
            adj_list = adj_matrix_to_adj_list(adj_matrix)
        elif representation == '3':
            adj_list = parse_adj_list(rows)
            adj_matrix = adj_list_to_adj_matrix(adj_list)
            inc_matrix = adj_matrix_to_inc_matrix(adj_matrix)
        else:
            print("Błąd: Nieznany wybór formatu. Powrót do menu głównego.")
            return
    except FileNotFoundError:
        print(f"Błąd: Nie znaleziono pliku '{filename}'.")
        return
    except ValueError as e:
        print(f"Błąd danych w pliku '{filename.name}': {e}")
        return

    print("\n--- Macierz sąsiedztwa ---")
    print_matrix(adj_matrix)
    print("\n--- Lista sąsiedztwa ---")
    print_adj_list(adj_list)
    print("\n--- Macierz incydencji ---")
    print_matrix(inc_matrix)

    draw_graph(adj_list, f"Wizualizacja grafu z pliku: {filename.name}")
