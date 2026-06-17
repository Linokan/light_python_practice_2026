from pathlib import Path


def scan_folder(folder):
    files_data = []

    for file_path in folder.rglob("*"):
        if file_path.is_file():

            files_data.append({
                "path": str(file_path),
                "size": file_path.stat().st_size,
                "extension": file_path.suffix,
            })

    return files_data