from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'AppleGeeks Lite'
    language = 'en'
    url = 'http://www.applegeeks.com/'
    start_date = '2006-04-18'
    history_capable_days = 30
    schedule = 'Mo,We,Fr'
    time_zone = -5
    rights = 'Mohammad Haque & Ananth Panagariya'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.applegeeks.com/rss/?cat=lite')
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img')
            title = entry.title.replace('AG Lite - ', '')
            return CrawlerResult(url, title)
