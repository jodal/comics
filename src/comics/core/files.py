from __future__ import annotations

import hashlib
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.core.files import File


def sha256sum(file: File) -> str:
    """The SHA-256 checksum of the file's contents, as a hex string."""
    digest = hashlib.sha256()
    for chunk in file.chunks():
        digest.update(chunk)
    return digest.hexdigest()
