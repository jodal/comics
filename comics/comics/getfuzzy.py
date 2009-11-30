from comics.aggregator.crawler import BaseComicsComComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Get Fuzzy'
    language = 'en'
    url = 'http://comics.com/get_fuzzy/'
    start_date = '1999-09-01'
    history_capable_date = '2009-05-26'
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = -5
    rights = 'Darby Conley'

class ComicCrawler(BaseComicsComComicCrawler):
    def crawl(self):
        self.crawl_helper('Get Fuzzy')
