from comics.core.exceptions import ComicsError

class StripAlreadyExists(ComicsError):
    """Exception raised when trying to save a strip that already exists"""
    def __str__(self):
        return 'Strip already exists (%s)' % self.value

class HistoryCapabilityError(ComicsError):
    """Base class for comic history capability exceptions"""
    def __str__(self):
        return 'Comic history capability error (%s)' % self.value

class NotHistoryCapable(HistoryCapabilityError):
    """Exception raised when a comic is not history capable"""
    def __str__(self):
        return 'Comic is not history capable (%s)' % self.value

class OutsideHistoryCapabilityRange(HistoryCapabilityError):
    """Exception raised when trying to crawl strips outside the comics' history
    capability"""
    def __str__(self):
        return 'Outside the history capable range (%s)' % self.value

class CrawlerError(ComicsError):
    """Base class for crawler exceptions"""
    def __str__(self):
        return 'Crawler error (%s)' % self.value

class StripURLNotFound(CrawlerError):
    """Exception raised when the URL for a strip is not found"""
    def __str__(self):
        return 'Strip URL not found (%s)' % self.value

class StripNotAnImage(CrawlerError):
    """Exception raised when the fetched file is not an image"""
    def __str__(self):
        return 'Strip not an image (%s)' % self.value
