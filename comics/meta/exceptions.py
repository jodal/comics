from comics.core.exceptions import ComicsError

class MetaError(ComicsError):
    """Base class for comics meta exceptions"""
    def __str__(self):
        return 'Comics meta error (%s)' % self.value
