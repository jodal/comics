import re

from comics.crawler.base import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Focus Shift'
    language = 'en'
    url = 'http://www.osnews.com/comics/'
    start_date = '2008-01-27'
    history_capable_date = '2008-01-27'
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 1
    rights = 'Thom Holwerda'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.parse_feed('http://osnews.com/files/comics.xml')

        for entry in self.feed.entries:
            if self.timestamp_to_date(entry.updated_parsed) == self.pub_date:
                self.title = entry.title
                m = re.match('.*src="([^"]+)".*', entry.summary)
                m = m.groups()
                self.url = m[0]
                return
