from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Nemi (db.no)'
    language = 'no'
    url = 'http://www.dagbladet.no/tegneserie/nemi/'
    start_date = '1997-01-01'
    rights = 'Lise Myhre'

class Crawler(CrawlerBase):
    history_capable_days = 14
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 1

    def crawl(self, pub_date):
        url = 'http://www.dagbladet.no/tegneserie/nemiarkiv/serve.php?%s' % (
            self.date_to_epoch(pub_date),)
        return CrawlerImage(url)
