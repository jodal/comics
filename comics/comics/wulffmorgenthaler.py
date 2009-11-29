from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Wulffmorgenthaler'
    language = 'en'
    url = 'http://www.wulffmorgenthaler.com/'
    start_date = '2001-01-01'
    history_capable_days = 10
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 1
    rights = 'Mikael Wulff & Anders Morgenthaler'

class ComicCrawler(BaseComicCrawler):
    def crawl(self):
        feed = self.parse_feed('http://feeds.feedburner.com/wulffmorgenthaler')
        for entry in feed.for_day(self.pub_date):
            self.url = entry.summary.src(
                'img[src^="http://www.wulffmorgenthaler.com/"]')
