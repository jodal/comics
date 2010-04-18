from comics.aggregator.crawler import PondusNoCrawlerBase
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'EON'
    language = 'no'
    url = 'http://pondus.no/#CartoonGallery'
    start_date = '2008-11-19'
    rights = 'Lars Lauvik'

class Crawler(PondusNoCrawlerBase):
    history_capable_days = 14
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'

    def crawl(self, pub_date):
        return self.crawl_helper('EON', pub_date)
