# encoding: utf-8

from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Veslemøy'
    language = 'no'
    url = 'http://www.side2.no/tegneserie/veslemoy/'
    start_date = '2008-11-14'
    history_capable_date = '2008-11-14'
    schedule = 'Mo,We,Fr'
    time_zone = 1
    rights = 'Vantina Nina Andreassen'

class ComicCrawler(BaseComicCrawler):
    def crawl(self):
        self.url = 'http://pub.tv2.no/nettavisen/tegneserie/pondus/veslemoy/%(date)s.jpg' % {
            'date': self.pub_date.strftime('%d%m%y'),
        }
