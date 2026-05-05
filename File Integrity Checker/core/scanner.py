import os
from core.hasher import calculate_hash

def scan_directory(directory, algorithm, ignore_extensions):
    file_hashes = {}

    for root, dirs, files in os.walk(directory):
        for file in files:
            if any(file.endswith(ext) for ext in ignore_extensions):
                continue

            path = os.path.join(root, file)

            try:
                file_hashes[path] = calculate_hash(path, algorithm)
            except Exception as e:
                print(f"Error scanning {path}: {e}")

    return file_hashes