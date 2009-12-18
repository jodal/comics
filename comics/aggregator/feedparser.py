from __future__ import absolute_import

import datetime as dt
import feedparser

from comics.aggregator.lxmlparser import LxmlParser

class FeedParser(object):
    def __init__(self, url):
        self.raw_feed = feedparser.parse(url)
        self.encoding = self.raw_feed.encoding or None

    def for_date(self, date):
        return [Entry(e, self.encoding) for e in self.raw_feed.entries
            if e.updated_parsed and dt.date(*e.updated_parsed[:3]) == date]

    def all(self):
        return [Entry(e, self.encoding) for e in self.raw_feed.entries]

class Entry(object):
    def __init__(self, entry, encoding=None):
        self.raw_entry = entry
        self.encoding = encoding
        if 'summary' in entry:
            self.summary = self.html(entry.summary)
        if 'content' in entry:
            self.content0 = self.html(entry.content[0].value)

    def __getattr__(self, name):
        attr = getattr(self.raw_entry, name)
        if isinstance(attr, str) and self.encoding is not None:
            attr = attr.decode(encoding)
        return attr

    def html(self, string):
        return LxmlParser(string=string)

    @property
    def tags(self):
        if not 'tags' in self.raw_entry:
            return []
        return [tag.term for tag in self.raw_entry.tags]
