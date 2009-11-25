import re

from comics.crawler.base import BaseComicCrawler
from comics.crawler.meta import BaseComicMeta
from comics.crawler.utils.lxmlparser import LxmlParser

class ComicMeta(BaseComicMeta):
    name = 'Cyanide and Happiness'
    language = 'en'
    url = 'http://www.explosm.net/comics/'
    start_date = '2005-01-26'
    history_capable_days = 7
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = -8
    rights = 'Kris Wilson, Rob DenBleyker, Matt Melvin, & Dave McElfatrick '

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.parse_feed('http://feeds.feedburner.com/Explosm')

        for entry in self.feed.entries:
            if entry.title == self.pub_date.strftime('%m.%d.%Y'):
                self.web_url = entry.link
                break

        if self.web_url is None:
            return

        page = LxmlParser(self.web_url)
        self.url = page.src('img[alt="Cyanide and Happiness, a daily webcomic"]')
