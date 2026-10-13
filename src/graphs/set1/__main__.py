"""Set 1 presentation menu: python -m graphs.set1"""
from graphs.menu import run_menu
from graphs.set1 import task1_representations, task3_random_graphs

TASKS = {
    "1": ("Zadanie 1 i 2: Wczytaj graf z pliku (konwersja + wizualizacja)", task1_representations.demo),
    "3a": ("Zadanie 3a: Generuj graf losowy G(n, p)", task3_random_graphs.demo_gnp),
    "3b": ("Zadanie 3b: Generuj graf losowy G(n, l)", task3_random_graphs.demo_gnl),
}


def main():
    run_menu("ZESTAW 1", TASKS)


if __name__ == "__main__":
    main()
