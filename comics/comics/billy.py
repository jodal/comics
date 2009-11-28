from comics.crawler.base import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Billy'
    language = 'no'
    url = 'http://www.billy.no/'
    start_date = '1950-01-01'
    history_capable_days = 6
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 1
    rights = 'Mort Walker'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.url = 'http://cserver.it-content.com/retriever.php?id=104&date=%(date)s' % {
            'date': self.pub_date.strftime('%Y%m%d'),
        }
