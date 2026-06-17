import hashlib


def calculate_file_hash(file_path):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        while True:
            data = file.read(8192)

            if not data:
                break

            sha256.update(data)

    return sha256.hexdigest()


def find_duplicates(files):
    duplicates = {}

    for file in files:
        file_hash = file["file_hash"]

        if file_hash not in duplicates:
            duplicates[file_hash] = []

        duplicates[file_hash].append(file["relative_path"])

    return {
        file_hash: paths
        for file_hash, paths in duplicates.items()
        if len(paths) > 1
    }