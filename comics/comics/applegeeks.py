from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'AppleGeeks'
    language = 'en'
    url = 'http://www.applegeeks.com/'
    start_date = '2003-01-01'
    history_capable_days = 30
    schedule = 'Mo,Th'
    time_zone = -5
    rights = 'Mohammad Haque & Ananth Panagariya'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.applegeeks.com/rss/?cat=comic')
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img').replace('thumb.gif', '.jpg')
            title = entry.title
            return CrawlerResult(url, title)
