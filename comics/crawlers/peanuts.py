from comics.crawler.base import BaseComicsComComicCrawler
from comics.crawler.meta import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Peanuts'
    language = 'en'
    url = 'http://www.peanuts.com/'
    start_date = '1950-10-02'
    end_date = '2000-02-13'
    history_capable_days = 32
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    rights = 'Charles M. Schulz'

class ComicCrawler(BaseComicsComComicCrawler):
    def _get_url(self):
        self._get_url_helper('Peanuts')
