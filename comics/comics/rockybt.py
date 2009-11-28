from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Rocky (bt.no)'
    language = 'no'
    url = 'http://www.bt.no/tegneserier/rocky/'
    start_date = '1998-01-01'
    history_capable_days = 162
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 1
    rights = 'Martin Kellerman'

class ComicCrawler(BaseComicCrawler):
    def crawl(self):
        self.url = 'http://images.bt.no/gfx/cartoons/rocky/%(date)s.gif' % {
            'date': self.pub_date.strftime('%d%m%y'),
        }
