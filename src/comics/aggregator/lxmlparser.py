import httpx
from lxml.html import fromstring

from comics.aggregator.exceptions import CrawlerError


class LxmlParser:
    def __init__(self, url=None, string=None, headers=None):
        self._retrieved_url = None

        if url is not None:
            self.root = self._parse_url(url, headers)
        elif string is not None:
            self.root = self._parse_string(string)
        else:
            raise LxmlParserException("Parser needs URL or string to operate on")

    def href(self, selector, default=None, allow_multiple=False):
        return self._get("href", selector, default, allow_multiple)

    def src(self, selector, default=None, allow_multiple=False):
        return self._get("src", selector, default, allow_multiple)

    def alt(self, selector, default=None, allow_multiple=False):
        return self._get("alt", selector, default, allow_multiple)

    def title(self, selector, default=None, allow_multiple=False):
        return self._get("title", selector, default, allow_multiple)

    def value(self, selector, default=None, allow_multiple=False):
        return self._get("value", selector, default, allow_multiple)

    def id(self, selector, default=None, allow_multiple=False):
        return self._get("id", selector, default, allow_multiple)

    def content(self, selector, default=None, allow_multiple=False):
        return self._get("content", selector, default, allow_multiple)

    def text(self, selector, default=None, allow_multiple=False):
        try:
            if allow_multiple:
                build_results = []
                for match in self._select(selector, allow_multiple):
                    build_results.append(self._decode(match.text_content()))
                return build_results
            else:
                return self._decode(self._select(selector).text_content())
        except DoesNotExist:
            if allow_multiple and default is None:
                return []
            return default

    def remove(self, selector):
        for element in self.root.cssselect(selector):
            element.drop_tree()

    def url(self):
        return self._retrieved_url

    def _get(self, attr, selector, default=None, allow_multiple=False):
        try:
            if allow_multiple:
                build_results = []
                for match in self._select(selector, allow_multiple):
                    build_results.append(self._decode(match).get(attr))
                return build_results
            else:
                return self._decode(self._select(selector).get(attr))
        except DoesNotExist:
            if allow_multiple and default is None:
                return []
            return default

    def _select(self, selector, allow_multiple=False):
        elements = self.root.cssselect(selector)

        if len(elements) == 0:
            raise DoesNotExist("Nothing matched the selector: %s" % selector)
        elif len(elements) > 1 and not allow_multiple:
            raise MultipleElementsReturned(
                "Selector matched %d elements: %s" % (len(elements), selector)
            )

        if allow_multiple:
            return elements
        else:
            return elements[0]

    def _parse_url(self, url, headers=None):
        response = httpx.get(url, headers=headers, follow_redirects=True)
        self._retrieved_url = str(response.url)
        content = response.content.replace(b"\x00", b"")
        root = self._parse_string(content)
        root.make_links_absolute(self._retrieved_url)
        return root

    def _parse_string(self, value):
        if len(value.strip()) == 0:
            value = "<xml />"
        return fromstring(value)

    def _decode(self, value):
        if isinstance(value, bytes):
            try:
                value = value.decode("utf-8")
            except UnicodeDecodeError:
                value = value.decode("iso-8859-1")
        return value


class LxmlParserException(CrawlerError):
    pass


class DoesNotExist(LxmlParserException):
    pass


class MultipleElementsReturned(LxmlParserException):
    pass
