from comics.aggregator.crawler import BaseComicsComComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Rose Is Rose'
    language = 'en'
    url = 'http://comics.com/rose_is_rose/'
    start_date = '1984-10-02'
    history_capable_date = '1995-10-09'
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = -5
    rights = 'Pat Brady'

class ComicCrawler(BaseComicsComComicCrawler):
    def _get_url(self):
        self._get_url_helper('Rose Is Rose')
