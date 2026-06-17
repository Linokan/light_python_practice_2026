from scanner import scan_folder


def compare_folders(source_folder, backup_folder):
    source_files = scan_folder(source_folder)
    backup_files = scan_folder(backup_folder)

    source_dict = {
        file["relative_path"]: file
        for file in source_files
    }

    backup_dict = {
        file["relative_path"]: file
        for file in backup_files
    }

    missing_files = []
    changed_files = []
    extra_files = []

    for path, source_file in source_dict.items():
        if path not in backup_dict:
            missing_files.append(path)
        else:
            backup_file = backup_dict[path]

            if source_file["file_hash"] != backup_file["file_hash"]:
                changed_files.append(path)

    for path in backup_dict:
        if path not in source_dict:
            extra_files.append(path)

    return {
        "missing": missing_files,
        "changed": changed_files,
        "extra": extra_files
    }