from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Dilbert'
    language = 'en'
    url = 'http://www.dilbert.com/'
    start_date = '1989-04-06'
    history_capable_days = 32
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    rights = 'Scott Adams'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        feed = self.parse_feed('http://feeds.feedburner.com/DilbertDailyStrip')
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img[src*="dilbert.com"]')
            return CrawlerResult(url)
