from comics.crawler.crawlers import BaseComicCrawler
from comics.crawler.meta import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Sinfest'
    language = 'en'
    url = 'http://www.sinfest.net/'
    start_date = '2001-01-17'
    history_capable_date = '2001-01-17'
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    rights = 'Tatsuya Ishida'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.url = 'http://www.sinfest.net/comikaze/comics/%(date)s.gif' % {
            'date': self.pub_date.strftime('%Y-%m-%d'),
        }
