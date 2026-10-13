"""Entry point: python -m graphs <set> [task]"""
import importlib
import pkgutil
import sys

import graphs


def print_usage():
    """Print usage and every available set with its tasks."""
    print("Użycie: python -m graphs <zestaw> [zadanie]   np. python -m graphs 2 1\n")
    set_names = sorted(
        (m.name for m in pkgutil.iter_modules(graphs.__path__) if m.ispkg and m.name.startswith("set")),
        key=lambda name: int(name[3:]),
    )
    for set_name in set_names:
        number = set_name[3:]
        tasks = importlib.import_module(f"graphs.{set_name}.__main__").TASKS
        print(f"Zestaw {number}:   python -m graphs {number}")
        for key, (label, _) in tasks.items():
            print(f"  python -m graphs {number} {key:<4} {label}")
        print()


def main(argv):
    if not argv:
        print_usage()
        return 1

    module_name = f"graphs.set{argv[0]}.__main__"
    try:
        set_module = importlib.import_module(module_name)
    except ModuleNotFoundError as e:
        if not module_name.startswith(e.name or "?"):
            raise
        print(f"Nie ma zestawu {argv[0]}.")
        return 1

    if len(argv) == 1:
        set_module.main()
        return 0

    task = set_module.TASKS.get(argv[1].lower())
    if task is None:
        print(f"Nie ma zadania {argv[1]} w zestawie {argv[0]}. Dostępne: {', '.join(set_module.TASKS)}")
        return 1
    try:
        task[1]()
    except (KeyboardInterrupt, EOFError):
        print("\nKoniec programu.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
