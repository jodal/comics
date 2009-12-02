from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Nemi (db.no)'
    language = 'no'
    url = 'http://www.dagbladet.no/tegneserie/nemi/'
    start_date = '1997-01-01'
    history_capable_days = 14
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 1
    rights = 'Lise Myhre'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        url = 'http://www.dagbladet.no/tegneserie/nemiarkiv/serve.php?%(date)s' % {
            'date': self.date_to_epoch(pub_date),
        }
        return CrawlerResult(url)
