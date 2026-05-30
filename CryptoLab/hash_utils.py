"""Hash generator utilities for MD5 and SHA-256."""

import hashlib


def generate_hash(algorithm: str, text: str) -> str:
    """Create a hash digest using the requested algorithm.

    Args:
        algorithm: Supported values are 'MD5' or 'SHA-256'.
        text: The source text to hash.

    Returns:
        The hexadecimal digest string for the selected algorithm.
    """
    if not text:
        raise ValueError("Text input is required for hashing.")

    normalized_algorithm = algorithm.strip().upper()
    encoded_text = text.encode("utf-8")

    if normalized_algorithm == "MD5":
        return hashlib.md5(encoded_text).hexdigest()
    if normalized_algorithm == "SHA-256":
        return hashlib.sha256(encoded_text).hexdigest()

    raise ValueError(f"Unsupported hash algorithm: {algorithm}")
