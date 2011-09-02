from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Hejibits'
    language = 'en'
    url = 'http://www.hejibits.com/'
    start_date = '2010-03-02'
    rights = 'John Kleckner'

class Crawler(CrawlerBase):
    history_capable_days = 90
    time_zone = -7

    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.hejibits.com/feed/')
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img[src*="/comics/"]')
            title = entry.title
            return CrawlerImage(url, title)
