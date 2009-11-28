from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Nemi (db.no)'
    language = 'no'
    url = 'http://www.dagbladet.no/tegneserie/nemi/'
    start_date = '1997-01-01'
    history_capable_days = 14
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 1
    rights = 'Lise Myhre'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.url = 'http://www.dagbladet.no/tegneserie/nemiarkiv/serve.php?%(date)s' % {
            'date': self.date_to_epoch(self.pub_date),
        }
