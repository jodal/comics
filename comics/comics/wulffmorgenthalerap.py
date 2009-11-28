from comics.crawler.base import BaseComicCrawler
from comics.crawler.meta import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Wulffmorgenthaler (ap.no)'
    language = 'no'
    url = 'http://www.aftenposten.no/tegneserier/'
    start_date = '2001-01-01'
    history_capable_days = 1
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 1
    rights = 'Mikael Wulff & Anders Morgenthaler'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        page = self.parse_page('http://www.aftenposten.no/tegneserier/')
        self.url = page.src('img#theCartoon')
