from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Dilbert'
    language = 'en'
    url = 'http://www.dilbert.com/'
    start_date = '1989-04-06'
    rights = 'Scott Adams'

class Crawler(CrawlerBase):
    history_capable_days = 32
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'

    def crawl(self, pub_date):
        feed = self.parse_feed('http://feeds.feedburner.com/DilbertDailyStrip')
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img[src*="dilbert.com"]')
            return CrawlerImage(url)
