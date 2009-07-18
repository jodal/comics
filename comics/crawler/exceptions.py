"""Exceptions used mainly when crawling the web for comics"""

class ComicsError(Exception):
    """Base class for all comic exceptions"""
    # Work around "message" being deprecated in Python 2.6
    _message = None
    def _get_message(self):
        return self._message
    def _set_message(self, message):
        self._message = message
    message = property(_get_message, _set_message)

class StripAlreadyExists(ComicsError):
    """Exception raised when trying to save a strip that already exists"""
    def __str__(self):
        return 'Strip already exists (%s)' % self.message

class HistoryCapabilityError(ComicsError):
    """Base class for comic history capability exceptions"""
    pass
class NotHistoryCapable(HistoryCapabilityError):
    """Exception raised when a comic is not history capable"""
    def __str__(self):
        return 'Comic is not history capable (%s)' % self.message
class OutsideHistoryCapabilityRange(HistoryCapabilityError):
    """Exception raised when trying to crawl strips outside the comics' history
    capability"""
    def __str__(self):
        return 'Outside the history capable range (%s)' % self.message

class CrawlerError(ComicsError):
    """Base class for crawler exceptions"""
    pass
class StripURLNotFound(CrawlerError):
    """Exception raised when the URL for a strip is not found"""
    def __str__(self):
        return 'Strip URL not found (%s)' % self.message
class StripNotAnImage(CrawlerError):
    """Exception raised when the fetched file is not an image"""
    def __str__(self):
        return 'Strip not an image (%s)' % self.message

class ComicsMetaError(ComicsError):
    """Base class for comics meta exceptions"""
    pass
