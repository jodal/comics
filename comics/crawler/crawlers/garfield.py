from comics.crawler.base import BaseComicCrawler
from comics.crawler.meta import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Garfield'
    language = 'en'
    url = 'http://www.garfield.com/'
    start_date = '1978-06-19'
    history_capable_days = 31
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = -5
    rights = 'Jim Davis'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.url = 'http://images.ucomics.com/comics/ga/%(year)s/ga%(date)s.gif' % {
            'year': self.pub_date.strftime('%Y'),
            'date': self.pub_date.strftime('%y%m%d'),
        }
