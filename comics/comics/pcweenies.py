from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'The PC Weenies'
    language = 'en'
    url = 'http://www.pcweenies.com/'
    start_date = '1998-10-21'
    rights = 'Krishna M. Sadasivam'

class Crawler(CrawlerBase):
    history_capable_days = 10
    schedule = 'Tu,Th,Sa'
    time_zone = -8

    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.pcweenies.com/feed/')
        for entry in feed.for_date(pub_date):
            if 'Comic' in entry.tags:
                title = entry.title
                url = entry.content0.src(u'img[src*="/comics/"]')
                return CrawlerImage(url, title)
