"""Set 4 presentation menu: python -m graphs.set4"""
from graphs.menu import run_menu
from graphs.set4 import task1_digraphs, task2_kosaraju, task3_bellman_ford, task4_johnson

TASKS = {
    "1": ("Zadanie 1: Digrafy - reprezentacje i losowy G(n, p)", task1_digraphs.demo),
    "2": ("Zadanie 2: Silnie spójne składowe (Kosaraju)", task2_kosaraju.demo),
    "3": ("Zadanie 3: Silnie spójny digraf z wagami + Bellman-Ford", task3_bellman_ford.demo),
    "4": ("Zadanie 4: Macierz odległości (Johnson)", task4_johnson.demo),
    "all": ("Całość: G(n, p) -> Kosaraju -> wagi -> Johnson na jednym grafie", task4_johnson.demo_all),
}


def main():
    run_menu("ZESTAW 4", TASKS)


if __name__ == "__main__":
    main()
