from comics.crawler.base import BaseComicCrawler
from comics.crawler.meta import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Nemi (bt.no)'
    language = 'no'
    url = 'http://www.bt.no/tegneserier/nemi/'
    start_date = '1997-01-01'
    history_capable_days = 162
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 1
    rights = 'Lise Myhre'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.url = 'http://images.bt.no/gfx/cartoons/nemi/%(date)s.gif' % {
            'date': self.pub_date.strftime('%d%m%y'),
        }
