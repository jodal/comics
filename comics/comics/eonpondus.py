from comics.aggregator.crawler import PondusNoCrawlerBase
from comics.comics.eon import Meta as EonMeta

class Meta(EonMeta):
    name = 'EON (pondus.no)'
    url = 'http://pondus.no/#CartoonGallery'

class Crawler(PondusNoCrawlerBase):
    history_capable_days = 14
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'

    def crawl(self, pub_date):
        return self.crawl_helper('EON', pub_date)
