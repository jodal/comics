from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Johnny Wander'
    language = 'en'
    url = 'http://www.johnnywander.com/'
    start_date = '2008-09-30'
    rights = 'Yuko Ota & Ananth Panagariya'

class Crawler(CrawlerBase):
    history_capable_days = 40
    schedule = 'Tu,Th'
    time_zone = -8

    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.johnnywander.com/feed')
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img')
            title = entry.title
            text = entry.summary.title('img')
            return CrawlerImage(url, title, text)
