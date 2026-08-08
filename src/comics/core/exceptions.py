class ComicsError(Exception):
    """Base class for all comic exceptions"""

    def __init__(self, value: object) -> None:
        self.value = value

    def __str__(self) -> str:
        return f"Generic comics error ({self.value})"


class MetadataError(ComicsError):
    """Base class for comic metadata exceptions"""

    def __str__(self) -> str:
        return f"Comics metadata error ({self.value})"
