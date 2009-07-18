from comics.crawler.base import BaseComicCrawler
from comics.crawler.meta import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Dilbert (bt.no)'
    language = 'no'
    url = 'http://www.bt.no/tegneserier/dilbert/'
    start_date = '1989-04-16'
    history_capable_date = '2005-10-28'
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 1
    rights = 'Scott Adams'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.url = 'http://images.bt.no/gfx/cartoons/dilbert/%(date)s.gif' % {
            'date': self.pub_date.strftime('%d%m%y'),
        }
