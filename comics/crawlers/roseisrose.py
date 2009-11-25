from comics.crawler.base import BaseComicsComComicCrawler
from comics.crawler.meta import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Rose Is Rose'
    language = 'en'
    url = 'http://www.roseisrose.com/'
    start_date = '1984-10-02'
    history_capable_days = 32
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    rights = 'Pat Brady'

class ComicCrawler(BaseComicsComComicCrawler):
    def _get_url(self):
        self._get_url_helper('Rose Is Rose')
