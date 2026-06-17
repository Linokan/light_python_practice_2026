from pathlib import Path


def scan_folder(folder):
    files_data = []

    for file_path in folder.rglob("*"):
        if file_path.is_file():
            stat = file_path.stat()

            files_data.append({
                "relative_path": str(file_path.relative_to(folder)),
                "size": stat.st_size,
                "modified_time": stat.st_mtime,
                "extension": file_path.suffix
            })

    return files_data