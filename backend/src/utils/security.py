import hashlib

def sha256_hash(value: str) -> str:
    return hashlib.sha256_hash(value.encode("utf-8")).hexdigest()