# encoding: utf-8

from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Morten M (vg.no)'
    language = 'no'
    url = 'http://www.vg.no/spesial/mortenm/'
    start_date = '1978-01-01'
    history_capable_days = 120
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 1
    rights = 'Morten M. Kristiansen'

class ComicCrawler(BaseComicCrawler):
    def crawl(self):
        self.url = 'http://static.vg.no/gfx/mortenm/output/%(year)s/%(month)s/%(year)-%(month)s-%(day).jpg' % {
            'year': self.pub_date.strftime("%Y"),
            'month': self.pub_date.strftime("%m"),
            'day': self.pub_date.strftime("%d"),
        }
