import argparse
from pathlib import Path

from db import init_db, save_files
from scanner import scan_folder
from duplicates import find_duplicates
from backup import compare_folders


def main():
    parser = argparse.ArgumentParser(
        description="Консольный индексатор папок"
    )

    parser.add_argument(
        "command",
        choices=["scan", "compare"],
        help="Команда: scan или compare"
    )

    parser.add_argument(
        "folder",
        help="Путь к основной папке"
    )

    parser.add_argument(
        "backup_folder",
        nargs="?",
        help="Путь к папке резервной копии"
    )

    parser.add_argument(
        "--ext",
        help="Фильтр по расширению"
    )

    args = parser.parse_args()
    folder = Path(args.folder)

    if not folder.exists():
        print("Ошибка: папка не существует")
        return

    if not folder.is_dir():
        print("Ошибка: указан путь не к папке")
        return
    
    if args.command == "compare":
        if not args.backup_folder:
            print("Ошибка: для compare нужно указать папку резервной копии")
            return

        backup_folder = Path(args.backup_folder)

        if not backup_folder.exists():
            print("Ошибка: папка резервной копии не существует")
            return

        if not backup_folder.is_dir():
            print("Ошибка: указан путь не к папке резервной копии")
            return

        result = compare_folders(folder, backup_folder)

        print("\nОтсутствующие файлы:")
        for path in result["missing"]:
            print(path)

        print("\nИзмененные файлы:")
        for path in result["changed"]:
            print(path)

        print("\nЛишние файлы:")
        for path in result["extra"]:
            print(path)

        return

    init_db()

    if args.command == "scan":
        files = scan_folder(folder, args.ext)

    print(f"Найдено файлов: {len(files)}")

    for file in files:
        print(file["relative_path"])
    
    save_files(files)

    duplicates = find_duplicates(files)

    print("\nДубликаты:")

    if not duplicates:
        print("Не найдены")
    else:
        for file_hash, paths in duplicates.items():
            print(f"\nХэш: {file_hash}")

            for path in paths:
                print(f"  {path}")

    print("Данные сохранены в SQLite")


if __name__ == "__main__":
    main()