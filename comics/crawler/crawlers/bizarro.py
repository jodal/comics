from comics.crawler.base import BaseComicCrawler
from comics.crawler.meta import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Bizarro'
    language = 'no'
    url = 'http://www.start.no/tegneserier/bizarro/'
    start_date = '1985-01-01'
    end_date = '2009-06-24' # No longer hosted at start.no
    history_capable_days = 30
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 1
    rights = 'Dan Piraro'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.url = 'http://g2.start.no/tegneserier/striper/bizarro/biz-striper/biz%(date)s.gif' % {
            'date': self.pub_date.strftime('%Y%m%d'),
        }
