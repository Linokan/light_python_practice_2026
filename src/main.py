import argparse
from pathlib import Path

from db import init_db, save_files

from scanner import scan_folder


def main():
    parser = argparse.ArgumentParser(
        description="Консольный индексатор папок"
    )

    parser.add_argument(
        "folder",
        help="Путь к папке для сканирования"
    )

    args = parser.parse_args()
    folder = Path(args.folder)

    if not folder.exists():
        print("Ошибка: папка не существует")
        return

    if not folder.is_dir():
        print("Ошибка: указан путь не к папке")
        return

    init_db()

    files = scan_folder(folder)

    print(f"Найдено файлов: {len(files)}")

    for file in files:
        print(file["relative_path"])
    
    save_files(files)

    print("Данные сохранены в SQLite")

    print("Программа запущена")
    print("Папка для сканирования:", folder)


if __name__ == "__main__":
    main()