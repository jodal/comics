import re

from comics.crawler.crawlers import BaseComicCrawler
from comics.crawler.meta import BaseComicMeta

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
                self.web_url = entry.link
                break

        if self.web_url is None:
            return

        self.parse_web_page()

        for image in self.web_page.imgs:
            if ('src' in image and 'alt' in image
                and image['alt'] == 'The Joy of Tech comic'):
                self.url = self.join_web_url(image['src'])
                return
