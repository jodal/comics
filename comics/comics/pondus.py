# encoding: utf-8

from comics.crawler.base import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Pondus (db.no)'
    language = 'no'
    url = 'http://www.dagbladet.no/tegneserie/pondus/'
    start_date = '1995-01-01'
    history_capable_days = 14
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 1
    rights = 'Frode Øverli'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.url = 'http://www.dagbladet.no/tegneserie/pondusarkiv/serve.php?%(date)s' % {
            'date': self.date_to_epoch(self.pub_date),
        }
