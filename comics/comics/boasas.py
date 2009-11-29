from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Boy on a Stick and Slither'
    language = 'en'
    url = 'http://www.boasas.com/'
    start_date = '1998-01-01'
    history_capable_days = 40
    schedule = 'Mo,We,Fr'
    time_zone = -5
    rights = 'Steven L. Cloud'

class ComicCrawler(BaseComicCrawler):
    def crawl(self):
        feed = self.parse_feed('http://www.boasas.com/boasas_rss.xml')
        for entry in feed.for_day(self.pub_date):
            self.url = entry.summary.src('img')
            self.title = entry.title
