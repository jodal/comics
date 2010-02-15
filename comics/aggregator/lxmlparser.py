from lxml.html import fromstring
import urllib2

from comics.aggregator.exceptions import CrawlerError

class LxmlParser(object):
    def __init__(self, url=None, string=None):
        self._retrived_url = None

        if url is not None:
            self.root = self._parse_url(url)
        elif string is not None:
            self.root = self._parse_string(string)
        else:
            raise LxmlParserException(
                'Parser needs URL or string to operate on')

    def href(self, selector, default=None, allowmultiple=False):
        return self._get('href', selector, default, allowmultiple)

    def src(self, selector, default=None, allowmultiple=False):
        return self._get('src', selector, default, allowmultiple)

    def alt(self, selector, default=None, allowmultiple=False):
        return self._get('alt', selector, default, allowmultiple)

    def title(self, selector, default=None, allowmultiple=False):
        return self._get('title', selector, default, allowmultiple)

    def value(self, selector, default=None, allowmultiple=False):
        return self._get('value', selector, default, allowmultiple)

    def text(self, selector, default=None, allowmultiple=False):
        try:
            if allowmultiple == False:
                return self._decode(self._select(selector).text_content())
            else:
                build_results = []
                the_matches = self._select(selector, allowmultiple)
                for the_match in the_matches:
                    build_results.append(self._decode(the_match.text_content()))
                return build_results
        except DoesNotExist:
            return default

    def remove(self, selector):
        for element in self.root.cssselect(selector):
            element.drop_tree()

    def url(self):
        return self._retrived_url

    def _get(self, attr, selector, default=None, allowmultiple=False):
        try:
            if allowmultiple == False:
                return self._decode(self._select(selector).get(attr))
            else:
                build_results = []
                the_matches = self._select(selector, allowmultiple)
                for the_match in the_matches:
                    build_results.append(self._decode(the_match).get(attr))
                return build_results
        except DoesNotExist:
            return default

    def _select(self, selector, allowmultiple=False):
        elements = self.root.cssselect(selector)

        if len(elements) == 0:
            raise DoesNotExist('Nothing matched the selector: %s' % selector)
        elif len(elements) > 1:
            # Don't return a multiple unless we allow it
            if allowmultiple == False:
                raise MultipleElementsReturned('Selector matched %d elements and allowmultiple is false: %s' %
                    (len(elements), selector))
            # ... otherwise, send back an array and assume upstream can handle it
            else:
                return elements

        return elements[0]

    def _parse_url(self, url):
        handle = urllib2.urlopen(url)
        content = handle.read()
        self._retrived_url = handle.geturl()
        handle.close()
        content = content.replace('\x00', '')
        root = self._parse_string(content)
        root.make_links_absolute(self._retrived_url)
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
