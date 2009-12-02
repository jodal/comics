# encoding: utf-8

from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Butternutsquash'
    language = 'en'
    url = 'http://www.butternutsquash.net/'
    start_date = '2003-04-16'
    history_capable_date = '2003-04-16'
    rights = 'Ramón Pérez & Rob Coughler'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        url = 'http://www.butternutsquash.net/comics/%(date)s.jpg' % {
            'date': pub_date.strftime('%Y-%m-%d'),
        }
        return CrawlerResult(url)
