from comics.aggregator.crawler import CrawlerBase, CrawlerResult
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

    def crawl(self, pub_date):
        url = 'http://www.somethingpositive.net/sp%s.gif' % (
            pub_date.strftime('%m%d%Y'),)
        return CrawlerResult(url)
