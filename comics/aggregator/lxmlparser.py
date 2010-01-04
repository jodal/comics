from lxml.html import fromstring
import urllib2

from comics.aggregator.exceptions import CrawlerError

class LxmlParser(object):
    def __init__(self, url=None, string=None):
        if url is not None:
            self.root = self._parse_url(url)
        elif string is not None:
            self.root = self._parse_string(string)
        else:
            raise LxmlParserException(
                'Parser needs URL or string to operate on')

    def text(self, selector, default=None):
        try:
            return self._decode(self.select(selector).text_content())
        except DoesNotExist:
            return default

    def href(self, selector, default=None):
        try:
            return self._decode(self.select(selector).get('href'))
        except DoesNotExist:
            return default

    def src(self, selector, default=None):
        try:
            return self._decode(self.select(selector).get('src'))
        except DoesNotExist:
            return default

    def alt(self, selector, default=None):
        try:
            return self._decode(self.select(selector).get('alt'))
        except DoesNotExist:
            return default

    def title(self, selector, default=None):
        try:
            return self._decode(self.select(selector).get('title'))
        except DoesNotExist:
            return default

    def remove(self, selector):
        for element in self.root.cssselect(selector):
            element.drop_tree()

    def select(self, selector):
        elements = self.root.cssselect(selector)

        if len(elements) == 0:
            raise DoesNotExist('Nothing matched the selector: %s' % selector)
        elif len(elements) > 1:
            raise MultipleElementsReturned('Selector matched %d elements: %s' %
                (len(elements), selector))

        return elements[0]

    def _parse_url(self, url):
        handle = urllib2.urlopen(url)
        content = handle.read()
        url = handle.geturl()
        handle.close()
        content = content.replace('\x00', '')
        root = self._parse_string(content)
        root.make_links_absolute(url)
        return root

    def _parse_string(self, string):
        if len(string) == 0:
            string = '<xml />'
        return fromstring(string)

    def _decode(self, string):
        if isinstance(string, str):
            try:
                string = string.decode('utf-8')
            except UnicodeDecodeError:
                string = string.decode('iso-8859-1')
        return string

class LxmlParserException(CrawlerError):
    pass

class DoesNotExist(LxmlParserException):
    pass

class MultipleElementsReturned(LxmlParserException):
    pass
