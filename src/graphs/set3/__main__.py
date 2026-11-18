"""Set 3 presentation menu: python -m graphs.set3"""
from graphs.menu import run_menu
from graphs.set3 import task1_connected_weighted, task2_dijkstra, task3_distance_matrix, task4_centers, task5_mst

TASKS = {
    "1": ("Zadanie 1: Generuj spójny graf losowy z wagami", task1_connected_weighted.demo),
    "2": ("Zadanie 2: Najkrótsze ścieżki (algorytm Dijkstry)", task2_dijkstra.demo),
    "3": ("Zadanie 3: Macierz odległości", task3_distance_matrix.demo),
    "4": ("Zadanie 4: Centrum grafu i centrum minimax", task4_centers.demo),
    "5": ("Zadanie 5: Minimalne drzewo rozpinające (Kruskal)", task5_mst.demo),
}


def main():
    run_menu("ZESTAW 3", TASKS)


if __name__ == "__main__":
    main()
