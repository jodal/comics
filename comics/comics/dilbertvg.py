from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Dilbert (vg.no)'
    language = 'no'
    url = 'http://www.vg.no/dilbert/'
    start_date = '1989-04-16'
    rights = 'Scott Adams'

class Crawler(CrawlerBase):
    history_capable_days = 1
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 1

    def crawl(self, pub_date):
        url = 'http://www.vg.no/grafikk/dilbert/dilbert-%s.gif' % (
            pub_date.strftime('%Y-%m-%d'),)
        return CrawlerResult(url)
