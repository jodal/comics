from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'ExtraLife'
    language = 'en'
    url = 'http://www.myextralife.com/'
    start_date = '2001-06-17'
    history_capable_date = '2001-06-17'
    schedule = 'Mo,We,Fr'
    time_zone = -7
    rights = 'Scott Johnson'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        url = 'http://www.myextralife.com/strips/%(date)s.jpg' % {
            'date': pub_date.strftime('%m-%d-%Y'),
        }
        return CrawlerResult(url)
