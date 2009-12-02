from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Diesel Sweeties (print)'
    language = 'en'
    url = 'http://www.dieselsweeties.com/'
    start_date = '2007-01-01'
    rights = 'Richard Stevens'

class Crawler(CrawlerBase):
    history_capable_date = '2007-01-01'
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = -5

    def crawl(self, pub_date):
        url = 'http://www.dieselsweeties.com/print/strips/ds%s.png' % (
            pub_date.strftime('%Y%m%d'),)
        return CrawlerResult(url)
