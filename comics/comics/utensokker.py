# encoding: utf-8

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Uten Sokker'
    language = 'no'
    url = 'http://nettserier.no/utensokker/'
    start_date = '2009-07-14'
    rights = 'Bjørnar Grandalen'

class Crawler(CrawlerBase):
    history_capable_date = '2009-07-14'
    schedule = 'Sa,Su'
    time_zone = 1

    def crawl(self, pub_date):
        url = 'http://nettserier.no/_striper/utensokker-%s.jpg' % (
            self.date_to_epoch(pub_date),)
        return CrawlerImage(url)
