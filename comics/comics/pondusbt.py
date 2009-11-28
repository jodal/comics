# encoding: utf-8

from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Pondus (bt.no)'
    language = 'no'
    url = 'http://www.bt.no/tegneserier/?type=pondus'
    start_date = '1995-01-01'
    history_capable_days = 14
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 1
    rights = 'Frode Øverli'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.url = 'http://images.bt.no/gfx/cartoons/pondus/%(date)s.gif' % {
            'date': self.pub_date.strftime('%d%m%y'),
        }
