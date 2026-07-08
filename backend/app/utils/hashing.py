from hashlib import sha256


def sha256_digest(data: bytes) -> str:
	hasher = sha256()
	hasher.update(data)
	return hasher.hexdigest()