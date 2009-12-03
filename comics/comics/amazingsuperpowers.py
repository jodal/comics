from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'AmazingSuperPowers'
    language = 'en'
    url = 'http://www.amazingsuperpowers.com/'
    start_date = '2007-09-24'
    rights = 'Wes & Tony'

class Crawler(CrawlerBase):
    history_capable_days = 21
    schedule = 'Mo,Th'
    time_zone = -5

    def crawl(self, pub_date):
        feed = self.parse_feed(
            'http://www.amazingsuperpowers.com/category/comics/feed/')
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img')
            title = entry.title
            text = entry.summary.title('img')
            return CrawlerResult(url, title, text)
