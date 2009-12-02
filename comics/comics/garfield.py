from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Garfield'
    language = 'en'
    url = 'http://www.garfield.com/'
    start_date = '1978-06-19'
    history_capable_days = 31
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = -5
    rights = 'Jim Davis'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        url = 'http://images.ucomics.com/comics/ga/%(year)s/ga%(date)s.gif' % {
            'year': pub_date.strftime('%Y'),
            'date': pub_date.strftime('%y%m%d'),
        }
        return CrawlerResult(url)
