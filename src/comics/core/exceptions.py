class ComicsError(Exception):
    """Base class for all comic exceptions"""

    def __init__(self, value: object) -> None:
        self.value = value

    def __str__(self) -> str:
        return f"Generic comics error ({self.value})"


class ComicDataError(ComicsError):
    """Base class for comic data exceptions"""

    def __str__(self) -> str:
        return f"Comics data error ({self.value})"
