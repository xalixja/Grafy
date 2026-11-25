from graphs.menu import run_menu
from graphs.set6 import task1_pagerank, task2_tsp

TASKS = {
    "1": ("PageRank", task1_pagerank.demo),
    "2": ("Komiwojażer", task2_tsp.demo),
}


def main():
    run_menu("ZESTAW 6", TASKS)


if __name__ == "__main__":
    main()
