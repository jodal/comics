from comics.crawler.base import BaseComicCrawler
from comics.crawler.meta import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Diesel Sweeties (print)'
    language = 'en'
    url = 'http://www.dieselsweeties.com/'
    start_date = '2007-01-01'
    history_capable_date = '2007-01-01'
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = -5
    rights = 'Richard Stevens'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.url = 'http://www.dieselsweeties.com/print/strips/ds%(date)s.png' \
        % {
            'date': self.pub_date.strftime('%Y%m%d'),
        }
