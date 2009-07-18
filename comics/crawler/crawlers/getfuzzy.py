from comics.crawler.crawlers import BaseComicsComComicCrawler
from comics.crawler.meta import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Get Fuzzy'
    language = 'en'
    url = 'http://www.comics.com/comics/getfuzzy/'
    start_date = '1999-09-01'
    history_capable_days = 32
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = -5
    rights = 'Darby Conley'

class ComicCrawler(BaseComicsComComicCrawler):
    def _get_url(self):
        self._get_url_helper('Get Fuzzy')
