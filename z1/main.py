from utils import load_matrix, print_matrix
import networkx as nx
import matplotlib.pyplot as plt
import random
from itertools import combinations

##### ZADANIE 1 #####

# Zamiana macierzy sąsiedztwa na listę sąsiedztwa
def adj_matrix_to_adj_list(adj_matrix):
    n = len(adj_matrix)
    adj_list = [[] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if adj_matrix[i][j]:
                adj_list[i].append(j)
    return adj_list

# Zamiana listy sąsiedztwa na macierz incydencji
def adj_list_to_inc_matrix(adj_list):
    n = len(adj_list)
    edges = set()

    for u in range(n):
        for v in adj_list[u]:
            edges.add((min(u, v), max(u, v)))

    edges = list(edges)
    k = len(edges)
    inc_matrix = [[0]*k for _ in range(n)]

    for i, (u, v) in enumerate(edges):
        inc_matrix[u][i] = 1
        inc_matrix[v][i] = 1

    return inc_matrix

# Zamiana macierzy incydencji na macierz sąsiedztwa
def inc_matrix_to_adj_matrix(inc_matrix):
    n = len(inc_matrix)
    k = len(inc_matrix[0])
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

# Zamiana macierzy incydencji na listę sąsiedztwa
def inc_matrix_to_adj_list(inc_matrix):
    adj_matrix = inc_matrix_to_adj_matrix(inc_matrix)
    return adj_matrix_to_adj_list(adj_matrix)

# Zamiana macierzy sąsiedztwa na macierz incydencji
def adj_matrix_to_inc_matrix(adj_matrix):
    adj_list = adj_matrix_to_adj_list(adj_matrix)
    return adj_list_to_inc_matrix(adj_list)

# Zamiana listy sąsiedztwa na macierz sąsiedztwa
def adj_list_to_adj_matrix(adj_list):
    inc_matrix = adj_list_to_inc_matrix(adj_list)
    return inc_matrix_to_adj_matrix(inc_matrix)

##### ZADANIE 2 #####
def draw_graph(adj_matrix, title):
    G = nx.Graph()
    n = len(adj_matrix)

    G.add_nodes_from(range(n))
    for i in range(n):
        for j in range(i + 1, n):
            if adj_matrix[i][j] == 1:
                G.add_edge(i, j)
                
    pos = nx.circular_layout(G)
    
    plt.figure()
    nx.draw(G, pos, with_labels=True, node_color='pink', node_size=600, font_size=14, edge_color='lightblue')
    plt.axis('equal')
    plt.suptitle(title, fontsize=14)
    plt.margins(0.1)
    plt.show()

##### ZADANIE 3 #####
# Generuje losowy graf G(n, p)
def generate_G_np(n, p):
    matrix = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if random.random() < p:
                matrix[i][j] = 1
                matrix[j][i] = 1
    return matrix

# # Generuje losowy graf G(n, l)
def generate_G_nl(n, l):
    max = n * (n-1) // 2
    if l > max or l < 0:
        print(f"\nDla {n} wierzchołków liczba krawędzi musi wynosić od 0 do {max}.")
        return []
    
    matrix = [[0]*n for _ in range(n)]

    all_edges = list(combinations(range(n), 2))
    random_edges = random.sample(all_edges, l)

    for i, j in random_edges:
        matrix[i][j] = 1
        matrix[j][i] = 1
        
    return matrix

while True:
    print("\n" + "="*40)
    print("1. Zadanie 1 i 2: Wczytaj graf z pliku (konwersja + wizualizacja)")
    print("2. Zadanie 3a: Generuj graf losowy G(n, p)")
    print("3. Zadanie 3b: Generuj graf losowy G(n, l)")
    print("4. Wyjście")
    print("="*40)
    
    choice = input("Wybierz opcję (1-4): ")
    
    if choice == '4':
        print("Zamykanie programu...")
        break
        
    elif choice == '1':
        filename = input("Podaj nazwę pliku: ")
        try:
            data = load_matrix(filename)
            print("\nJaki format danych znajduje się w pliku?")
            print("1. Macierz sąsiedztwa")
            print("2. Macierz incydencji")
            print("3. Lista sąsiedztwa")
            format = input("Wybierz format (1-3): ")

            if format == '1':
                adj_matrix = data
                adj_list = adj_matrix_to_adj_list(adj_matrix)
                inc_matrix = adj_matrix_to_inc_matrix(adj_matrix)    
            elif format == '2':
                inc_matrix = data
                adj_matrix = inc_matrix_to_adj_matrix(inc_matrix)
                adj_list = adj_matrix_to_adj_list(adj_matrix)
            elif format == '3':
                adj_list = [row[1:] for row in data]
                print(adj_list)
                inc_matrix = adj_list_to_inc_matrix(adj_list)
                adj_matrix = inc_matrix_to_adj_matrix(inc_matrix)
            else:
                print("Błąd: Nieznany wybór formatu. Powrót do menu głównego.")
                continue

            
            print("\n--- Macierz sąsiedztwa ---")
            print_matrix(adj_matrix)
            print("\n--- Lista sąsiedztwa ---")
            print_matrix(adj_list)
            print("\n--- Macierz incydencji ---")
            print_matrix(inc_matrix)
            
            draw_graph(adj_matrix, f"Wizualizacja grafu z pliku: {filename}")
            
        except FileNotFoundError:
            print(f"Błąd: Nie znaleziono pliku '{filename}'.")
        except Exception as e:
            print(f"Wystąpił błąd podczas wczytywania: {e}")
            
    elif choice == '2':
        try:
            n = int(input("Podaj liczbę wierzchołków (n): "))
            p = float(input("Podaj prawdopodobieństwo (p) [0.0 - 1.0]: "))
            gnp_matrix = generate_G_np(n, p)
            
            print("\n--- Macierz sąsiedztwa G(n, p) ---")
            print_matrix(gnp_matrix)
            draw_graph(gnp_matrix, f"Wizualizacja G(n={n}, p={p})")
        except ValueError:
            print("Błąd: Wprowadzono niepoprawne dane. Użyj liczb.")
    elif choice == '3':
        try:
            n = int(input("Podaj liczbę wierzchołków (n): "))
            l = int(input("Podaj liczbę krawędzi (l): "))
            gnl_matrix = generate_G_nl(n, l)
            
            if gnl_matrix:
                print("\n--- Macierz sąsiedztwa G(n, l) ---")
                print_matrix(gnl_matrix)
                draw_graph(gnl_matrix, f"Wizualizacja G(n={n}, l={l})")
        except ValueError:
            print("Błąd: Wprowadzono niepoprawne dane. Użyj liczb całkowitych.")
    else:
        print("Nieznana opcja. Wybierz numer od 1 do 4.")