from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Garfield'
    language = 'en'
    url = 'http://www.garfield.com/'
    start_date = '1978-06-19'
    rights = 'Jim Davis'

class Crawler(CrawlerBase):
    history_capable_days = 31
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = -5

    def crawl(self, pub_date):
        url = 'http://images.ucomics.com/comics/ga/%s.gif' % (
            pub_date.strftime('%Y/ga%y%m%d'),)
        return CrawlerResult(url)
