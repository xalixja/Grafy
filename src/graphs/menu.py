"""Shared presentation helpers used by every set: task menu and data file picker."""
from pathlib import Path

# <repo>/data  (this file lives in <repo>/src/graphs/menu.py)
DATA_DIR = Path(__file__).resolve().parents[2] / "data"


def choose_data_file(set_name):
    """List files from data/<set_name>/ and let the user pick one by number.
    A non-numeric answer is treated as a path typed by hand. Returns a path or None."""
    files = sorted(p for p in (DATA_DIR / set_name).glob("*") if p.is_file())

    print(f"\nPliki w data/{set_name}/:")
    for i, path in enumerate(files, start=1):
        print(f"{i}. {path.name}")
    if not files:
        print("(brak plików)")

    answer = input("Wybierz numer pliku (albo wpisz ścieżkę): ").strip()
    if answer.isdigit():
        index = int(answer)
        if 1 <= index <= len(files):
            return files[index - 1]
        print("Nieprawidłowy numer pliku.")
        return None
    return Path(answer) if answer else None


def run_menu(title, tasks):
    """tasks: dict {key: (label, callable)}; loops until 'q' or Ctrl+C / Ctrl+D."""
    try:
        _menu_loop(title, tasks)
    except (KeyboardInterrupt, EOFError):
        print("\nKoniec programu.")


def _menu_loop(title, tasks):
    while True:
        print("\n" + "=" * 40)
        print(title)
        for key, (label, _) in tasks.items():
            print(f"{key}. {label}")
        print("q. Wyjście")
        print("=" * 40)

        choice = input("Wybierz opcję: ").strip().lower()
        if choice == "q":
            print("Zamykanie programu...")
            break

        task = tasks.get(choice)
        if task is None:
            print("Nieznana opcja.")
            continue
        task[1]()
