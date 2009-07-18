from comics.crawler.base import BaseComicCrawler
from comics.crawler.meta import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Lagunen'
    language = 'no'
    url = 'http://www.start.no/tegneserier/lagunen/'
    start_date = '1991-05-13'
    history_capable_days = 30
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 1
    rights = 'Jim Toomey'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.url = 'http://g2.start.no/tegneserier/striper/lagunen/lag-striper/lag%(date)s.gif' % {
            'date': self.pub_date.strftime('%Y%m%d'),
        }
