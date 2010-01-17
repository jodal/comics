from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Rocky (db.no)'
    language = 'no'
    url = 'http://www.dagbladet.no/tegneserie/rocky/'
    start_date = '1998-01-01'
    rights = 'Martin Kellerman'

class Crawler(CrawlerBase):
    history_capable_days = 14
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 1

    def crawl(self, pub_date):
        url = 'http://www.dagbladet.no/tegneserie/rockyarkiv/serve.php?%s' % (
            self.date_to_epoch(pub_date),)
        return CrawlerImage(url)
