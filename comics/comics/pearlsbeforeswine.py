from comics.crawler.base import BaseComicsComComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Pearls Before Swine'
    language = 'en'
    url = 'http://comics.com/pearls_before_swine/'
    start_date = '2001-12-30'
    history_capable_date = '2002-01-06'
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = -5
    rights = 'Stephan Pastis'

class ComicCrawler(BaseComicsComComicCrawler):
    def _get_url(self):
        self._get_url_helper('Pearls Before Swine')
