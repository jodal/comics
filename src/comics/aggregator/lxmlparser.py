from __future__ import annotations

from typing import TYPE_CHECKING, overload

import httpx
from lxml.html import fromstring

from comics.aggregator.exceptions import CrawlerError

if TYPE_CHECKING:
    from lxml.html import HtmlElement


class LxmlParser:
    """Parser for web pages and HTML fragments, using CSS selectors.

    The parser is initialized with either a `url` to fetch and parse, or a
    `string` of HTML to parse. Relative URLs in the document are automatically
    expanded to absolute URLs, so e.g. a `src` of `/comics/2008-04-13.png`
    is returned as `http://www.example.com/comics/2008-04-13.png`.

    All extraction methods take a CSS `selector` to match elements. In the
    event that the selector doesn't match any elements, `default` is
    returned.

    If the selector matches multiple elements, one of two things will happen:

    - Singular methods, e.g.
      [`src()`][comics.aggregator.lxmlparser.LxmlParser.src], raise a
      `MultipleElementsReturned` exception.
    - Plural methods, e.g.
      [`srcs()`][comics.aggregator.lxmlparser.LxmlParser.srcs], return a list
      of zero or more values.
    """

    _retrieved_url: str | None
    root: HtmlElement

    def __init__(
        self,
        url: str | None = None,
        string: str | None = None,
        headers: dict[str, str] | None = None,
    ):
        self._retrieved_url = None

        if url is not None:
            self.root = self._parse_url(url, headers)
        elif string is not None:
            self.root = self._parse_string(string)
        else:
            raise LxmlParserException("Parser needs URL or string to operate on")

    @overload
    def href(self, selector: str, *, default: str) -> str: ...

    @overload
    def href(self, selector: str, *, default: str | None = None) -> str | None: ...

    def href(self, selector: str, *, default: str | None = None) -> str | None:
        """Return the `href` attribute of the element matching `selector`."""
        return self._get_one("href", selector, default=default)

    def hrefs(self, selector: str) -> list[str]:
        """Return the `href` attribute of the elements matching `selector`."""
        return self._get_all("href", selector)

    @overload
    def src(self, selector: str, *, default: str) -> str: ...

    @overload
    def src(self, selector: str, *, default: str | None = None) -> str | None: ...

    def src(self, selector: str, *, default: str | None = None) -> str | None:
        """Return the `src` attribute of the element matching `selector`."""
        return self._get_one("src", selector, default=default)

    def srcs(self, selector: str) -> list[str]:
        """Return the `src` attribute of the elements matching `selector`."""
        return self._get_all("src", selector)

    @overload
    def alt(self, selector: str, *, default: str) -> str: ...

    @overload
    def alt(self, selector: str, *, default: str | None = None) -> str | None: ...

    def alt(self, selector: str, *, default: str | None = None) -> str | None:
        """Return the `alt` attribute of the element matching `selector`."""
        return self._get_one("alt", selector, default=default)

    def alts(self, selector: str) -> list[str]:
        """Return the `alt` attribute of the elements matching `selector`."""
        return self._get_all("alt", selector)

    @overload
    def title(self, selector: str, *, default: str) -> str: ...

    @overload
    def title(self, selector: str, *, default: str | None = None) -> str | None: ...

    def title(self, selector: str, *, default: str | None = None) -> str | None:
        """Return the `title` attribute of the element matching `selector`."""
        return self._get_one("title", selector, default=default)

    def titles(self, selector: str) -> list[str]:
        """Return the `title` attribute of the elements matching `selector`."""
        return self._get_all("title", selector)

    @overload
    def value(self, selector: str, *, default: str) -> str: ...

    @overload
    def value(self, selector: str, *, default: str | None = None) -> str | None: ...

    def value(self, selector: str, *, default: str | None = None) -> str | None:
        """Return the `value` attribute of the element matching `selector`."""
        return self._get_one("value", selector, default=default)

    def values(self, selector: str) -> list[str]:
        """Return the `value` attribute of the elements matching `selector`."""
        return self._get_all("value", selector)

    @overload
    def attr(self, attr: str, selector: str, *, default: str) -> str: ...

    @overload
    def attr(
        self,
        attr: str,
        selector: str,
        *,
        default: str | None = None,
    ) -> str | None: ...

    def attr(
        self,
        attr: str,
        selector: str,
        *,
        default: str | None = None,
    ) -> str | None:
        """Return the given `attr` attribute of the element matching `selector`."""
        return self._get_one(attr, selector, default=default)

    def attrs(self, attr: str, selector: str) -> list[str]:
        """Return the given `attr` attribute of the elements matching `selector`."""
        return self._get_all(attr, selector)

    @overload
    def id(self, selector: str, *, default: str) -> str: ...

    @overload
    def id(self, selector: str, *, default: str | None = None) -> str | None: ...

    def id(self, selector: str, *, default: str | None = None) -> str | None:
        """Return the `id` attribute of the element matching `selector`."""
        return self._get_one("id", selector, default=default)

    def ids(self, selector: str) -> list[str]:
        """Return the `id` attribute of the elements matching `selector`."""
        return self._get_all("id", selector)

    @overload
    def content(self, selector: str, *, default: str) -> str: ...

    @overload
    def content(self, selector: str, *, default: str | None = None) -> str | None: ...

    def content(self, selector: str, *, default: str | None = None) -> str | None:
        """Return the `content` attribute of the element matching `selector`."""
        return self._get_one("content", selector, default=default)

    def contents(self, selector: str) -> list[str]:
        """Return the `content` attribute of the elements matching `selector`."""
        return self._get_all("content", selector)

    @overload
    def text(self, selector: str, *, default: str) -> str: ...

    @overload
    def text(self, selector: str, *, default: str | None = ...) -> str | None: ...

    def text(
        self,
        selector: str,
        *,
        default: str | None = None,
    ) -> list[str] | str | None:
        """Return the text contained by the element matching `selector`."""
        return self._get_one("text", selector, default=default)

    def texts(self, selector: str) -> list[str]:
        """Return a list of the text contained by the elements matching `selector`."""
        return self._get_all("text", selector)

    def remove(self, selector: str) -> None:
        """Remove the elements matching `selector` from the parsed document."""
        for element in self.root.cssselect(selector):
            element.drop_tree()

    def url(self) -> str | None:
        """Return the URL of the parsed page, after following any redirects."""
        return self._retrieved_url

    @overload
    def _get_one(
        self,
        attr: str,
        selector: str,
        *,
        default: str,
    ) -> str: ...

    @overload
    def _get_one(
        self,
        attr: str,
        selector: str,
        *,
        default: str | None = ...,
    ) -> str | None: ...

    def _get_one(
        self,
        attr: str,
        selector: str,
        *,
        default: str | None = None,
    ) -> str | None:
        if (el := self._select_one(selector)) is None:
            return default
        if (value := el.text_content() if attr == "text" else el.get(attr)) is None:
            return default
        return value

    def _get_all(self, attr: str, selector: str) -> list[str]:
        try:
            return [
                self._decode(value)
                for el in self._select_all(selector)
                if (value := el.text_content() if attr == "text" else el.get(attr))
            ]
        except DoesNotExist:
            return []

    def _select_one(self, selector: str) -> HtmlElement | None:
        match self.root.cssselect(selector):
            case []:
                return None
            case [element]:
                return element
            case elements:
                msg = f"Selector matched {len(elements)} elements: {selector}"
                raise MultipleElementsReturned(msg)

    def _select_all(self, selector: str) -> list[HtmlElement]:
        return self.root.cssselect(selector)

    def _parse_url(
        self,
        url: str,
        headers: dict[str, str] | None = None,
    ) -> HtmlElement:
        response = httpx.get(url, headers=headers, follow_redirects=True)
        self._retrieved_url = str(response.url)
        content = response.content.replace(b"\x00", b"")
        root = self._parse_string(content)
        root.make_links_absolute(self._retrieved_url)
        return root

    def _parse_string(self, value: str | bytes) -> HtmlElement:
        if len(value.strip()) == 0:
            value = "<xml />"
        return fromstring(value)

    def _decode(self, value: str | bytes) -> str:
        if isinstance(value, bytes):
            try:
                return value.decode("utf-8")
            except UnicodeDecodeError:
                return value.decode("iso-8859-1")
        return value


class LxmlParserException(CrawlerError):
    pass


class DoesNotExist(LxmlParserException):
    pass


class MultipleElementsReturned(LxmlParserException):
    pass
