from comics.crawler.crawlers import BaseComicsComComicCrawler
from comics.crawler.meta import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Pearls Before Swine'
    language = 'en'
    url = 'http://www.comics.com/comics/pearls/'
    start_date = '2001-12-30'
    history_capable_days = 32
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = -8
    rights = 'Stephan Pastis'

class ComicCrawler(BaseComicsComComicCrawler):
    def _get_url(self):
        self._get_url_helper('Pearls Before Swine')
