from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Dilbert'
    language = 'en'
    url = 'http://www.dilbert.com/'
    start_date = '1989-04-06'
    history_capable_days = 32
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    rights = 'Scott Adams'

class ComicCrawler(BaseComicCrawler):
    def crawl(self):
        feed = self.parse_feed('http://feeds.feedburner.com/DilbertDailyStrip')
        for entry in feed.for_date(self.pub_date):
            self.url = entry.summary.src('img[src*="dilbert.com"]')
