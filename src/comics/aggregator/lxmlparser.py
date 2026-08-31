from __future__ import annotations

from typing import TYPE_CHECKING, overload

import httpx
from lxml.html import fromstring

from comics.core.exceptions import ComicsError

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

    Pass `first=True` to a singular method to take the first match in
    document order instead of raising, for pages that legitimately match
    several elements.

    To extract several values from the same part of a document, use
    [`element()`][comics.aggregator.lxmlparser.LxmlParser.element] or
    [`elements()`][comics.aggregator.lxmlparser.LxmlParser.elements] to scope
    a parser to it.
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
    def href(
        self,
        selector: str,
        *,
        default: str,
        first: bool = False,
    ) -> str: ...

    @overload
    def href(
        self,
        selector: str,
        *,
        default: str | None = None,
        first: bool = False,
    ) -> str | None: ...

    def href(
        self,
        selector: str,
        *,
        default: str | None = None,
        first: bool = False,
    ) -> str | None:
        """Return the `href` attribute of the element matching `selector`."""
        return self._get_one("href", selector, default=default, first=first)

    def hrefs(self, selector: str) -> list[str]:
        """Return the `href` attribute of the elements matching `selector`."""
        return self._get_all("href", selector)

    @overload
    def src(
        self,
        selector: str,
        *,
        default: str,
        first: bool = False,
    ) -> str: ...

    @overload
    def src(
        self,
        selector: str,
        *,
        default: str | None = None,
        first: bool = False,
    ) -> str | None: ...

    def src(
        self,
        selector: str,
        *,
        default: str | None = None,
        first: bool = False,
    ) -> str | None:
        """Return the `src` attribute of the element matching `selector`."""
        return self._get_one("src", selector, default=default, first=first)

    def srcs(self, selector: str) -> list[str]:
        """Return the `src` attribute of the elements matching `selector`."""
        return self._get_all("src", selector)

    @overload
    def alt(
        self,
        selector: str,
        *,
        default: str,
        first: bool = False,
    ) -> str: ...

    @overload
    def alt(
        self,
        selector: str,
        *,
        default: str | None = None,
        first: bool = False,
    ) -> str | None: ...

    def alt(
        self,
        selector: str,
        *,
        default: str | None = None,
        first: bool = False,
    ) -> str | None:
        """Return the `alt` attribute of the element matching `selector`."""
        return self._get_one("alt", selector, default=default, first=first)

    def alts(self, selector: str) -> list[str]:
        """Return the `alt` attribute of the elements matching `selector`."""
        return self._get_all("alt", selector)

    @overload
    def title(
        self,
        selector: str,
        *,
        default: str,
        first: bool = False,
    ) -> str: ...

    @overload
    def title(
        self,
        selector: str,
        *,
        default: str | None = None,
        first: bool = False,
    ) -> str | None: ...

    def title(
        self,
        selector: str,
        *,
        default: str | None = None,
        first: bool = False,
    ) -> str | None:
        """Return the `title` attribute of the element matching `selector`."""
        return self._get_one("title", selector, default=default, first=first)

    def titles(self, selector: str) -> list[str]:
        """Return the `title` attribute of the elements matching `selector`."""
        return self._get_all("title", selector)

    @overload
    def value(
        self,
        selector: str,
        *,
        default: str,
        first: bool = False,
    ) -> str: ...

    @overload
    def value(
        self,
        selector: str,
        *,
        default: str | None = None,
        first: bool = False,
    ) -> str | None: ...

    def value(
        self,
        selector: str,
        *,
        default: str | None = None,
        first: bool = False,
    ) -> str | None:
        """Return the `value` attribute of the element matching `selector`."""
        return self._get_one("value", selector, default=default, first=first)

    def values(self, selector: str) -> list[str]:
        """Return the `value` attribute of the elements matching `selector`."""
        return self._get_all("value", selector)

    @overload
    def attr(
        self,
        attr: str,
        selector: str,
        *,
        default: str,
        first: bool = False,
    ) -> str: ...

    @overload
    def attr(
        self,
        attr: str,
        selector: str,
        *,
        default: str | None = None,
        first: bool = False,
    ) -> str | None: ...

    def attr(
        self,
        attr: str,
        selector: str,
        *,
        default: str | None = None,
        first: bool = False,
    ) -> str | None:
        """Return the given `attr` attribute of the element matching `selector`."""
        return self._get_one(attr, selector, default=default, first=first)

    def attrs(self, attr: str, selector: str) -> list[str]:
        """Return the given `attr` attribute of the elements matching `selector`."""
        return self._get_all(attr, selector)

    @overload
    def id(
        self,
        selector: str,
        *,
        default: str,
        first: bool = False,
    ) -> str: ...

    @overload
    def id(
        self,
        selector: str,
        *,
        default: str | None = None,
        first: bool = False,
    ) -> str | None: ...

    def id(
        self,
        selector: str,
        *,
        default: str | None = None,
        first: bool = False,
    ) -> str | None:
        """Return the `id` attribute of the element matching `selector`."""
        return self._get_one("id", selector, default=default, first=first)

    def ids(self, selector: str) -> list[str]:
        """Return the `id` attribute of the elements matching `selector`."""
        return self._get_all("id", selector)

    @overload
    def content(
        self,
        selector: str,
        *,
        default: str,
        first: bool = False,
    ) -> str: ...

    @overload
    def content(
        self,
        selector: str,
        *,
        default: str | None = None,
        first: bool = False,
    ) -> str | None: ...

    def content(
        self,
        selector: str,
        *,
        default: str | None = None,
        first: bool = False,
    ) -> str | None:
        """Return the `content` attribute of the element matching `selector`."""
        return self._get_one("content", selector, default=default, first=first)

    def contents(self, selector: str) -> list[str]:
        """Return the `content` attribute of the elements matching `selector`."""
        return self._get_all("content", selector)

    @overload
    def text(
        self,
        selector: str,
        *,
        default: str,
        first: bool = False,
    ) -> str: ...

    @overload
    def text(
        self,
        selector: str,
        *,
        default: str | None = None,
        first: bool = False,
    ) -> str | None: ...

    def text(
        self,
        selector: str,
        *,
        default: str | None = None,
        first: bool = False,
    ) -> str | None:
        """Return the text contained by the element matching `selector`."""
        return self._get_one("text", selector, default=default, first=first)

    def texts(self, selector: str) -> list[str]:
        """Return a list of the text contained by the elements matching `selector`."""
        return self._get_all("text", selector)

    def element(self, selector: str, *, first: bool = False) -> LxmlParser | None:
        """Return a parser scoped to the element matching `selector`.

        Selectors used on the returned parser match the element itself as
        well as its descendants, so a scoped parser can both read the
        element's own attributes and dig further into it:

        ```python
        for row in page.elements("tr"):
            if row.text("td.date") != date_string:
                continue
            title = row.text("td.title a")
        ```

        Returns `None` if the selector doesn't match any element.
        """
        element = self._select_one(selector, first=first)
        if element is None:
            return None
        return self._scoped(element)

    def elements(self, selector: str) -> list[LxmlParser]:
        """Return a parser scoped to each of the elements matching `selector`."""
        return [self._scoped(element) for element in self._select_all(selector)]

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
        first: bool = False,
    ) -> str: ...

    @overload
    def _get_one(
        self,
        attr: str,
        selector: str,
        *,
        default: str | None = ...,
        first: bool = False,
    ) -> str | None: ...

    def _get_one(
        self,
        attr: str,
        selector: str,
        *,
        default: str | None = None,
        first: bool = False,
    ) -> str | None:
        if (el := self._select_one(selector, first=first)) is None:
            return default
        if (value := el.text_content() if attr == "text" else el.get(attr)) is None:
            return default
        return value

    def _get_all(self, attr: str, selector: str) -> list[str]:
        return [
            value
            for el in self._select_all(selector)
            if (value := el.text_content() if attr == "text" else el.get(attr))
        ]

    def _scoped(self, element: HtmlElement) -> LxmlParser:
        parser = LxmlParser.__new__(LxmlParser)
        parser._retrieved_url = self._retrieved_url
        parser.root = element
        return parser

    def _select_one(self, selector: str, *, first: bool = False) -> HtmlElement | None:
        match self.root.cssselect(selector):
            case []:
                return None
            case [element]:
                return element
            case [element, *_] if first:
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


class LxmlParserException(ComicsError):
    pass


class MultipleElementsReturned(LxmlParserException):
    pass
