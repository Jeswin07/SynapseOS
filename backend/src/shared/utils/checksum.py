import hashlib
from typing import BinaryIO


def calculate_sha256(
    file: BinaryIO,
) -> str:
    """
    Calculate SHA256 checksum.
    """

    sha256 = hashlib.sha256()

    file.seek(0)

    while chunk := file.read(1024 * 1024):
        sha256.update(chunk)

    file.seek(0)

    return sha256.hexdigest()