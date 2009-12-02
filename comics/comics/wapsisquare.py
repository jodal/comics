from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Wapsi Square'
    language = 'en'
    url = 'http://wapsisquare.com/'
    start_date = '2001-09-09'
    rights = 'Paul Taylor'

class Crawler(CrawlerBase):
    history_capable_days = 14
    schedule = 'Mo,Tu,We,Th,Fr'

    def crawl(self, pub_date):
        feed = self.parse_feed('http://wapsisquare.com/feed/')
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img')
            title = entry.title
            return CrawlerResult(url, title)
