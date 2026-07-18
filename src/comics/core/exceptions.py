class ComicsError(Exception):
    """Base class for all comic exceptions"""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"Generic comics error ({self.value})"


class ComicDataError(ComicsError):
    """Base class for comic data exceptions"""

    def __str__(self):
        return f"Comics data error ({self.value})"
