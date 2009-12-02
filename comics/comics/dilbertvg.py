from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Dilbert (vg.no)'
    language = 'no'
    url = 'http://www.vg.no/dilbert/'
    start_date = '1989-04-16'
    history_capable_days = 1
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 1
    rights = 'Scott Adams'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        url = 'http://www.vg.no/grafikk/dilbert/dilbert-%(date)s.gif' % {
            'date': pub_date.strftime('%Y-%m-%d'),
        }
        return CrawlerResult(url)
