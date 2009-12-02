from lxml.html import parse, fromstring

from comics.aggregator.exceptions import CrawlerError

class LxmlParser(object):
    def __init__(self, url=None, string=None):
        if url is not None:
            self.root = parse(url).getroot()
            self.root.make_links_absolute(url)
        elif string is not None:
            if len(string) == 0:
                string = '<xml />'
            self.root = fromstring(string)
        else:
            raise LxmlParserException(
                'Parser needs URL or string to operate on')

    def text(self, selector, default=None):
        try:
            return self.select(selector).text_content()
        except DoesNotExist:
            return default

    def src(self, selector, default=None):
        try:
            return self.select(selector).get('src')
        except DoesNotExist:
            return default

    def alt(self, selector, default=None):
        try:
            return self.select(selector).get('alt')
        except DoesNotExist:
            return default

    def title(self, selector, default=None):
        try:
            return self.select(selector).get('title')
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

class LxmlParserException(CrawlerError):
    pass

class DoesNotExist(LxmlParserException):
    pass

class MultipleElementsReturned(LxmlParserException):
    pass
