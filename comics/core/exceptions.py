class ComicsError(Exception):
    """Base class for all comic exceptions"""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return 'Generic comics error (%s)' % self.value


class ComicDataError(ComicsError):
    """Base class for comic data exceptions"""
    def __str__(self):
        return 'Comics data error (%s)' % self.value
