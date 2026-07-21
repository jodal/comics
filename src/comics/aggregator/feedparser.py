import datetime as dt
import warnings
from typing import Any

import feedparser

from comics.aggregator.lxmlparser import LxmlParser


class FeedParser:
    """Parser for RSS and Atom feeds.

    The parser is initialized with the feed URL to fetch and parse, typically
    through
    [`Crawler.parse_feed()`][comics.aggregator.crawler.CrawlerBase.parse_feed].
    """

    def __init__(self, url: str) -> None:
        self.raw_feed = feedparser.parse(url)

        bozo_exception = self.raw_feed.get("bozo_exception")
        if bozo_exception is not None and not isinstance(
            bozo_exception, feedparser.NonXMLContentType
        ):
            raise bozo_exception

        self.encoding: str | None = None
        if hasattr(self.raw_feed, "encoding") and self.raw_feed.encoding:
            self.encoding = self.raw_feed.encoding

    def for_date(self, date: dt.date) -> list["Entry"]:
        """Return all feed entries published or updated at `date`."""
        with warnings.catch_warnings():
            # feedparser 5.1.2 issues a warning whenever we use updated_parsed
            warnings.simplefilter("ignore")
            return [
                Entry(e, self.encoding)
                for e in self.raw_feed.entries
                if (
                    hasattr(e, "published_parsed")
                    and e.published_parsed
                    and dt.date(*e.published_parsed[:3]) == date
                )
                or (
                    hasattr(e, "updated_parsed")
                    and e.updated_parsed
                    and dt.date(*e.updated_parsed[:3]) == date
                )
            ]

    def all(self) -> list["Entry"]:
        """Return all feed entries."""
        return [Entry(e, self.encoding) for e in self.raw_feed.entries]


class Entry:
    """A feed entry, as returned by the feed parser.

    This is really a combination of the popular
    [feedparser](https://github.com/kurtmckee/feedparser) library and
    [`LxmlParser`][comics.aggregator.lxmlparser.LxmlParser]. It can do
    anything *feedparser* can do, and in addition you can use the
    [`LxmlParser`][comics.aggregator.lxmlparser.LxmlParser] methods on feed
    fields which contain HTML, like
    [`summary`][comics.aggregator.feedparser.Entry.summary] and
    [`content0`][comics.aggregator.feedparser.Entry.content0].
    """

    summary: LxmlParser
    """The entry's summary, with
    [`LxmlParser`][comics.aggregator.lxmlparser.LxmlParser] methods available
    for HTML parsing.

    This is the most frequently used entry field. Example usage:

    ```python
    url = entry.summary.src("img")
    title = entry.summary.alt("img")
    ```

    Only present if the feed entry has a summary.
    """

    content0: LxmlParser
    """The same as *feedparser*'s `content[0].value` field, but with
    [`LxmlParser`][comics.aggregator.lxmlparser.LxmlParser] methods available
    for HTML parsing.

    For some crawlers, this is where the interesting stuff is found. Only
    present if the feed entry has content.
    """

    def __init__(
        self,
        entry: feedparser.FeedParserDict,
        encoding: str | None = None,
    ) -> None:
        self.raw_entry = entry
        self.encoding = encoding
        if "summary" in entry:
            self.summary = self.html(entry.summary)
        if "content" in entry:
            self.content0 = self.html(entry.content[0].value)

    def __getattr__(self, name: str) -> Any:
        attr = getattr(self.raw_entry, name)
        if isinstance(attr, bytes) and self.encoding is not None:
            attr = attr.decode(self.encoding)
        return attr

    def html(self, value: str | bytes) -> LxmlParser:
        """Wrap `value` in a [`LxmlParser`][comics.aggregator.lxmlparser.LxmlParser].

        If you need to parse HTML in any other fields than
        [`summary`][comics.aggregator.feedparser.Entry.summary] and
        [`content0`][comics.aggregator.feedparser.Entry.content0], you can
        apply this method on the field, like it is applied on a feed entry's
        title field here:

        ```python
        title = entry.html(entry.title).text("h1")
        ```
        """
        if isinstance(value, bytes):
            value = value.decode(self.encoding or "utf-8")
        return LxmlParser(string=value)

    @property
    def tags(self) -> list[str]:
        """List of tags associated with the entry."""
        if "tags" not in self.raw_entry:
            return []
        return [tag.term for tag in self.raw_entry.tags]
