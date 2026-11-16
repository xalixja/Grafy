"""Set 5 presentation menu: python -m graphs.set5"""
from graphs.menu import run_menu
from graphs.set5 import task1_flow_network, task2_ford_fulkerson

TASKS = {
    "1": ("Zadanie 1: Losowa sieć przepływowa (warstwy, przepustowości)", task1_flow_network.demo),
    "2": ("Zadanie 2: Maksymalny przepływ (Ford-Fulkerson + BFS = Edmonds-Karp)", task2_ford_fulkerson.demo),
}


def main():
    run_menu("ZESTAW 5", TASKS)


if __name__ == "__main__":
    main()
