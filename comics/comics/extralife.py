from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'ExtraLife'
    language = 'en'
    url = 'http://www.myextralife.com/'
    start_date = '2001-06-17'
    rights = 'Scott Johnson'

class Crawler(CrawlerBase):
    history_capable_date = '2001-06-17'
    schedule = 'Mo,We,Fr'
    time_zone = -7

    def crawl(self, pub_date):
        url = 'http://www.myextralife.com/comics/%s.jpg' % (
            pub_date.strftime('%Y-%m-%d'),)
        return CrawlerResult(url)
