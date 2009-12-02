from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Wulffmorgenthaler'
    language = 'en'
    url = 'http://www.wulffmorgenthaler.com/'
    start_date = '2001-01-01'
    rights = 'Mikael Wulff & Anders Morgenthaler'

class Crawler(CrawlerBase):
    history_capable_days = 10
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 1

    def crawl(self, pub_date):
        feed = self.parse_feed('http://feeds.feedburner.com/wulffmorgenthaler')
        for entry in feed.for_date(pub_date):
            url = entry.summary.src(
                'img[src^="http://www.wulffmorgenthaler.com/"]')
            return CrawlerResult(url)
