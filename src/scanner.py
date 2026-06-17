from pathlib import Path


def scan_folder(folder, extension_filter=None):
    files_data = []

    for file_path in folder.rglob("*"):
        if ".git" in file_path.parts:
            continue

        if "__pycache__" in file_path.parts:
            continue

        if file_path.is_file():

            if extension_filter and file_path.suffix != extension_filter:
                continue

            stat = file_path.stat()

            files_data.append({
                "relative_path": str(file_path.relative_to(folder)),
                "size": stat.st_size,
                "modified_time": stat.st_mtime,
                "extension": file_path.suffix
            })

    return files_data