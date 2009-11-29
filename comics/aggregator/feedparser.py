from __future__ import absolute_import

import datetime as dt
import feedparser
from types import StringTypes

from comics.aggregator.lxmlparser import LxmlParser

class FeedParser(object):
    def __init__(self, url):
        self.raw_feed = feedparser.parse(url)

    def for_date(self, date):
        return [Entry(e) for e in self.raw_feed.entries
            if e.updated_parsed and dt.date(*e.updated_parsed[:3]) == date]

    def all(self):
        return [Entry(e) for e in self.raw_feed.entries]

class Entry(object):
    def __init__(self, entry):
        self.raw_entry = entry
        if 'summary' in entry:
            self.summary = self.html(entry.summary)
        if 'content' in entry:
            self.content0 = self.html(entry.content[0].value)

    def __getattr__(self, name):
        return getattr(self.raw_entry, name)

    def html(self, string):
        return LxmlParser(string=string)

    @property
    def tags(self):
        if not 'tags' in self.raw_entry:
            return []
        return [tag.term for tag in self.raw_entry.tags]
