"""Set 6, task 2: Euclidean TSP via simulated annealing with 2-opt."""
from math import dist, exp, isfinite
from pathlib import Path
from random import Random
import matplotlib.pyplot as plt

from graphs.menu import DATA_DIR


def read_points(path):
    points = []
    for number, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
        if not line.strip():
            continue
        try:
            x, y = map(float, line.split())
            if not (isfinite(x) and isfinite(y)):
                raise ValueError
        except ValueError as exc:
            raise ValueError(f"Oczekiwano dwóch skończonych współrzędnych w wierszu {number}.") from exc
        points.append((x, y))
    return points


def tour_length(points, tour):
    """Sum the tour length, including the edge back to the start."""
    return sum(dist(points[u], points[v]) for u, v in zip(tour, tour[1:] + tour[:1]))


def simulated_annealing(points, iterations=10_000, runs=5, seed=None):
    n = len(points)
    if n < 3 or iterations < 1 or runs < 1:
        raise ValueError("Potrzeba co najmniej trzech punktów i dodatnich parametrów wyżarzania.")
    best = list(range(n))
    best_length = tour_length(points, best)
    if n == 3:
        return best, best_length

    distances = [[dist(a, b) for b in points] for a in points]
    rng = Random(seed)
    for run in range(runs):
        tour = best.copy()
        if run % 2:
            rng.shuffle(tour)
        length = tour_length(points, tour)
        for level in range(100, 1, -1):
            temperature = 0.001 * level ** 2
            for _ in range(iterations):
                i = rng.randrange(n)
                j = (i + rng.randrange(2, n - 1)) % n
                if i > j:
                    i, j = j, i
                a, b = tour[i], tour[i + 1]
                c, d = tour[j], tour[(j + 1) % n]
                delta = distances[a][c] + distances[b][d] - distances[a][b] - distances[c][d]
                if delta <= 0 or rng.random() < exp(-delta / temperature):
                    tour[i + 1:j + 1] = reversed(tour[i + 1:j + 1])
                    length += delta
                    if length < best_length:
                        length = tour_length(points, tour)
                        if length < best_length:
                            best, best_length = tour.copy(), length
    return best, best_length


def plot_tours(points, initial, best):
    figure, axes = plt.subplots(1, 2, figsize=(12, 5), constrained_layout=True)
    for axis, title, tour in zip(axes, ("Cykl początkowy", "Najlepszy znaleziony cykl"), (initial, best)):
        xs, ys = zip(*(points[v] for v in tour + tour[:1]))
        axis.plot(xs, ys, "-o", markersize=3, linewidth=0.9)
        axis.set_title(f"{title}\nDługość: {tour_length(points, tour):.3f}")
        axis.set(xlabel="x", ylabel="y", aspect="equal")
        axis.grid(alpha=0.25)
    return figure


def demo():
    answer = input("Plik ze współrzędnymi (Enter = xqf131.dat): ").strip()
    path = Path(answer) if answer else DATA_DIR / "set6" / "xqf131.dat"
    try:
        points = read_points(path)
        best, length = simulated_annealing(points, seed=6)
    except (OSError, ValueError) as exc:
        print(f"Błąd: {exc}")
        return

    initial = list(range(len(points)))
    print(f"Liczba punktów: {len(points)}")
    print(f"Długość cyklu początkowego: {tour_length(points, initial):.3f}")
    print(f"Długość najkrótszego znalezionego cyklu: {length:.3f}")
    import matplotlib.pyplot as plt

    plot_tours(points, initial, best)
    plt.show(block=True)
