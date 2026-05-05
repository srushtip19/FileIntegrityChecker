import hashlib

def calculate_hash(filepath, algorithm):
    hash_func = getattr(hashlib, algorithm)()

    with open(filepath, 'rb') as f:
        while chunk := f.read(4096):
            hash_func.update(chunk)

    return hash_func.hexdigest()