from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Least I Could Do'
    language = 'en'
    url = 'http://www.leasticoulddo.com/'
    start_date = '2003-02-10'
    history_capable_date = '2003-02-10'
    schedule = 'Mo,Tu,We,Th,Fr,Sa'
    time_zone = -5
    rights = 'Ryan Sohmer & Lar deSouza'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        url = 'http://archive.leasticoulddo.com/strips/%(date)s.gif' % {
            'date': pub_date.strftime('%Y%m%d'),
        }
        return CrawlerResult(url)
