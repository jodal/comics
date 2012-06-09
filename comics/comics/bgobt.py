from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Business Guys on Business Trips'
    language = 'en'
    url = 'http://www.businessguysonbusinesstrips.com/'
    start_date = '2007-07-12'
    end_date = '2011-11-23'
    active = False
    rights = '"Managing Director"'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass # Comic no longer published
