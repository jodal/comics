from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'EON'
    language = 'no'
    url = 'http://www.nettavisen.no/tegneserie/striper/'
    start_date = '2008-11-19'
    rights = 'Lars Lauvik'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass # Comic no longer published
