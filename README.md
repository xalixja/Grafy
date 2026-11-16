# Grafy
Zestawy zadań z przedmiotu Grafy i ich zastosowania.

## Konfiguracja
```
uv sync
```

## Uruchamianie
```
uv run python -m graphs <zestaw> [zadanie]

uv run python -m graphs 1        # menu zestawu 1
uv run python -m graphs 1 3a     # zestaw 1, zadanie 3a
uv run python -m graphs.set2     # menu zestawu 2 (równoważne: python -m graphs 2)
```
Zadania wczytujące graf z pliku wyświetlają ponumerowaną listę plików z `data/setN/` (wybór numerem); można też wpisać własną ścieżkę.

### Zestaw 1
| komenda | zadanie |
|---|---|
| `python -m graphs 1 1`  | zad. 1 + 2: wczytanie grafu z pliku, konwersja reprezentacji, rysunek na okręgu |
| `python -m graphs 1 3a` | zad. 3a: losowy graf G(n, p) |
| `python -m graphs 1 3b` | zad. 3b: losowy graf G(n, l) |

### Zestaw 2
| komenda | zadanie |
|---|---|
| `python -m graphs 2 1` | zad. 1: ciąg graficzny (Havel-Hakimi) + konstrukcja grafu |
| `python -m graphs 2 2` | zad. 2: randomizacja krawędzi z zachowaniem stopni (rysunek przed/po) |
| `python -m graphs 2 3` | zad. 3: spójne składowe (DFS), największa składowa, rysunek w kolorach składowych |
| `python -m graphs 2 4` | zad. 4: losowy graf eulerowski + cykl Eulera (algorytm Fleury'ego) |
| `python -m graphs 2 5` | zad. 5: losowy graf k-regularny (warunki, Havel-Hakimi, randomizacja) |
| `python -m graphs 2 6` | zad. 6: sprawdzanie hamiltonowskości grafu (DFS z nawrotami), cykl Hamiltona |

### Zestaw 4
| komenda | zadanie |
|---|---|
| `python -m graphs 4 1`   | zad. 1: digrafy - reprezentacje (lista, macierz sąsiedztwa, macierz incydencji), losowy G(n, p) |
| `python -m graphs 4 2`   | zad. 2: silnie spójne składowe (algorytm Kosaraju) |
| `python -m graphs 4 3`   | zad. 3: losowy silnie spójny digraf z wagami, algorytm Bellmana-Forda |
| `python -m graphs 4 4`   | zad. 4: macierz odległości (algorytm Johnsona); Enter = przykład z rys. 2, sprawdzany z listingiem 4 |
| `python -m graphs 4 all` | całość na jednym grafie: G(n, p) -> Kosaraju -> wagi -> Johnson |

### Zestaw 5
| komenda | zadanie |
|---|---|
| `python -m graphs 5 1` | zad. 1: losowa warstwowa sieć przepływowa (N warstw, 2N dodatkowych łuków, c ∈ [1, 10]), rysunek warstwami |
| `python -m graphs 5 2` | zad. 2: maksymalny przepływ – Ford-Fulkerson + BFS (Edmonds-Karp), ścieżki krok po kroku, minimalny przekrój |

## Struktura
```
data/setN/                 dane wejściowe do zestawu N
src/graphs/menu.py         wspólne menu prezentacji
src/graphs/setN/taskK_*.py zadanie K z zestawu N: funkcje + demo()
src/graphs/setN/__main__.py menu prezentacji zestawu N (tylko jego zadania)
```
Zestawy importują wyłącznie z zestawów wcześniejszych (np. set2 korzysta z set1).
