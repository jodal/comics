from comics.aggregator.crawler import PondusNoCrawlerBase
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'Helt Nils'
    language = 'no'
    url = 'http://www.pondus.no/'
    rights = 'Nils Ofstad'

class Crawler(PondusNoCrawlerBase):
    schedule = 'We,Sa'

    def crawl(self, pub_date):
        return self.crawl_helper('20060')


