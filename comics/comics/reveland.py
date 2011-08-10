from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Reveland'
    language = 'no'
    url = 'http://reveland.nettserier.no/'
    start_date = '2007-03-20'
    rights = 'Jorunn Hanto-Haugse'

class Crawler(CrawlerBase):
    history_capable_days = 90
    schedule = None
    time_zone = 1

    def crawl(self, pub_date):
        url = 'http://reveland.nettserier.no/_striper/reveland-%s.jpg' % (
            self.date_to_epoch(pub_date),)
        return CrawlerImage(url)
