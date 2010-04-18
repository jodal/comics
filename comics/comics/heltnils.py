from comics.aggregator.crawler import PondusNoCrawlerBase
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Helt Nils'
    language = 'no'
    url = 'http://pondus.no/#CartoonGallery'
    rights = 'Nils Ofstad'

class Crawler(PondusNoCrawlerBase):
    history_capable_days = 7 * 7 # weeks
    schedule = 'Tu,Fr'

    def crawl(self, pub_date):
        return self.crawl_helper('Helt-Nils', pub_date)


