import networkx as nx
import matplotlib.pyplot as plt

# Wczytywanie macierzy z pliku
def load_matrix(filename):
    matrix = []
    with open(filename, 'r') as file:
        for line in file:
            row = [int(x) for x in line.split()]
            matrix.append(row)
    return matrix

# Wypisywanie macierzy
def print_matrix(matrix):
    n = len(matrix)
    for i in range(n):
        print(f" {str(i).rjust(3)} | {matrix[i]}")


# Rysowanie grafu
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
    plt.title(title, fontsize=14)
    plt.show()