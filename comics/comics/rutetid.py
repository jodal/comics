# encoding: utf-8

from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Rutetid'
    language = 'no'
    url = 'http://www.dagbladet.no/tegneserie/rutetid/'
    history_capable_days = 15
    schedule = 'Fr,Sa,Su'
    time_zone = 1
    rights = 'Frode Øverli'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.url = 'http://www.dagbladet.no/tegneserie/rutetidarkiv/serve.php?%(date)s' % {
            'date': self.date_to_epoch(self.pub_date),
        }
