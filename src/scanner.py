from pathlib import Path

from duplicates import calculate_file_hash


def scan_folder(folder, extension_filter=None):
    files_data = []

    scan_recursive(
        folder,
        folder,
        extension_filter,
        files_data
    )

    return files_data


def scan_recursive(current_folder, root_folder, extension_filter, files_data):
    for item in current_folder.iterdir():

        if item.name == ".git":
            continue

        if item.name == "__pycache__":
            continue

        if item.is_dir():
            scan_recursive(
                item,
                root_folder,
                extension_filter,
                files_data
            )

        elif item.is_file():

            if extension_filter and item.suffix != extension_filter:
                continue

            stat = item.stat()

            files_data.append({
                "relative_path": str(item.relative_to(root_folder)),
                "size": stat.st_size,
                "modified_time": stat.st_mtime,
                "extension": item.suffix,
                "file_hash": calculate_file_hash(item)
            })