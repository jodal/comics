import re

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Not Invented Here'
    language = 'en'
    url = 'http://notinventedhe.re/'
    start_date = '2009-09-21'
    rights = 'Bill Barnes and Paul Southworth'

class Crawler(CrawlerBase):
    history_capable_date = '2009-09-21'
    time_zone = 0

    def crawl(self, pub_date):
        url = 'http://thiswas.notinventedhe.re/on/%s' % \
            pub_date.strftime('%Y-%m-%d')
        return CrawlerImage(url)
