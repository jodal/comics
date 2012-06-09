from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Magpie Luck'
    language = 'en'
    url = 'http://magpieluck.com/'
    start_date = '2009-07-30'
    end_date = '2011-09-08'
    active = False
    rights = 'Katie Sekelsky, CC BY-NC-SA 3.0'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass # Comic no longer published
