from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'M'
    language = 'no'
    url = 'http://www.dagbladet.no/tegneserie/m'
    start_date = '2003-02-10'
    end_date = '2012-01-13'
    active = False
    rights = 'Mads Eriksen'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass # Comic no longer published
