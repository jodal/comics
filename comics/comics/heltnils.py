from comics.aggregator.crawler import PondusNoCrawlerBase
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Helt Nils'
    language = 'no'
    url = 'http://www.pondus.no/'
    rights = 'Nils Ofstad'

class Crawler(PondusNoCrawlerBase):
    schedule = 'Mo,Fr'

    def crawl(self, pub_date):
        return self.crawl_helper('20060')


