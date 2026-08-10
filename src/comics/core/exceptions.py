class ComicsError(Exception):
    """Base class for all comic exceptions"""


class MetadataError(ComicsError):
    """Raised when a comic module does not describe a valid comic"""
