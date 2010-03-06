from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Kiwiblitz'
    language = 'en'
    url = 'http://www.kiwiblitz.com/'
    start_date = '2009-04-18'
    rights = 'Mary Cagle'

class Crawler(CrawlerBase):
    history_capable_days = 32
    schedule = 'Tu,Th'
    time_zone = -8

    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.kiwiblitz.com/?feed=rss2')
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img[src*="/comics/"]')
            title = entry.summary.alt('img[src*="/comics/"]')
            return CrawlerImage(url, title)
