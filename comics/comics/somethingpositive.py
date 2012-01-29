from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Something Positive'
    language = 'en'
    url = 'http://www.somethingpositive.net/'
    start_date = '2001-12-19'
    rights = 'R. K. Milholland'

class Crawler(CrawlerBase):
    history_capable_date = '2001-12-19'
    schedule = 'Mo,Tu,We,Th,Fr'
    time_zone = -6

    def crawl(self, pub_date):
        url = 'http://www.somethingpositive.net/sp%s.png' % (
            pub_date.strftime('%m%d%Y'),)
        return CrawlerImage(url)
