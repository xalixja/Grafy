"""Set 2 presentation menu: python -m graphs.set2"""
from graphs.menu import run_menu
from graphs.set2 import task1_graphic_sequence, task2_randomization

TASKS = {
    "1": ("Zadanie 1: Ciąg graficzny (Havel-Hakimi)", task1_graphic_sequence.demo),
    "2": ("Zadanie 2: Randomizacja krawędzi (ab, cd -> ad, bc)", task2_randomization.demo),
}


def main():
    run_menu("ZESTAW 2", TASKS)


if __name__ == "__main__":
    main()
