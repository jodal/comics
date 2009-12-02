from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Boy on a Stick and Slither'
    language = 'en'
    url = 'http://www.boasas.com/'
    start_date = '1998-01-01'
    history_capable_days = 40
    schedule = 'Mo,We,Fr'
    time_zone = -5
    rights = 'Steven L. Cloud'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.boasas.com/boasas_rss.xml')
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img')
            title = entry.title
            return CrawlerResult(url, title)
