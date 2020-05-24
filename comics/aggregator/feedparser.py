from __future__ import absolute_import

import datetime
import warnings

import feedparser

from comics.aggregator.lxmlparser import LxmlParser


class FeedParser(object):
    def __init__(self, url):
        self.raw_feed = feedparser.parse(url)
        if 'bozo_exception' in self.raw_feed:
            raise self.raw_feed['bozo_exception']
        self.encoding = None
        if hasattr(self.raw_feed, "encoding") and self.raw_feed.encoding:
            self.encoding = self.raw_feed.encoding

    def for_date(self, date):
        with warnings.catch_warnings():
            # feedparser 5.1.2 issues a warning whenever we use updated_parsed
            warnings.simplefilter("ignore")
            return [
                Entry(e, self.encoding)
                for e in self.raw_feed.entries
                if (
                    hasattr(e, "published_parsed")
                    and e.published_parsed
                    and datetime.date(*e.published_parsed[:3]) == date
                )
                or (
                    hasattr(e, "updated_parsed")
                    and e.updated_parsed
                    and datetime.date(*e.updated_parsed[:3]) == date
                )
            ]

    def all(self):
        return [Entry(e, self.encoding) for e in self.raw_feed.entries]


class Entry(object):
    def __init__(self, entry, encoding=None):
        self.raw_entry = entry
        self.encoding = encoding
        if "summary" in entry:
            self.summary = self.html(entry.summary)
        if "content" in entry:
            self.content0 = self.html(entry.content[0].value)

    def __getattr__(self, name):
        attr = getattr(self.raw_entry, name)
        if isinstance(attr, str) and self.encoding is not None:
            attr = attr.decode(self.encoding)
        return attr

    def html(self, string):
        if isinstance(string, str) and self.encoding is not None:
            string = string.decode(self.encoding)
        return LxmlParser(string=string)

    @property
    def tags(self):
        if "tags" not in self.raw_entry:
            return []
        return [tag.term for tag in self.raw_entry.tags]
