import re

from comics.crawler.base import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'The Joy of Tech'
    language = 'en'
    url = 'http://www.geekculture.com/joyoftech/'
    start_date = '2000-08-14'
    history_capable_days = 30
    schedule = 'Mo,We,Fr'
    time_zone = -5
    rights = 'Geek Culture'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.parse_feed('http://www.joyoftech.com/joyoftech/jotblog/atom.xml')
        for entry in self.feed.entries:
            if (re.match('^JoT[ #]*\d.*', entry.title)
                    and self.timestamp_to_date(entry.updated_parsed)
                    == self.pub_date):
                page = self.parse_page(entry.link)
                self.url = page.src('img[alt="The Joy of Tech comic"]')
