from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Reveland'
    language = 'no'
    url = 'http://nettserier.no/reveland/'
    start_date = '2007-03-20'
    rights = 'Jorunn Hanto-Haugse'

class Crawler(CrawlerBase):
    history_capable_days = 180
    schedule = None
    time_zone = 1

    def crawl(self, pub_date):
        feed = self.parse_feed('http://nettserier.no/reveland/rss/')
        for entry in feed.for_date(pub_date):
            url = entry.html(entry.description).src('img')
            return CrawlerImage(url)
