"""Key file management helpers for CryptoLab."""

from pathlib import Path


def save_key(file_path: str, key: bytes) -> None:
    """Save a Fernet key to a file in binary mode."""
    if not key:
        raise ValueError("No key available to save.")
    if not file_path:
        raise ValueError("A valid file path is required.")

    path = Path(file_path)
    with path.open("wb") as key_file:
        key_file.write(key)


def load_key(file_path: str) -> bytes:
    """Load a Fernet key from a file."""
    if not file_path:
        raise ValueError("A valid file path is required.")

    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Key file not found: {file_path}")

    with path.open("rb") as key_file:
        loaded_key = key_file.read().strip()

    if not loaded_key:
        raise ValueError("Loaded key file is empty.")

    return loaded_key
