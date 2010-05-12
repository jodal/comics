from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = "Daryl Cagle's Political Blog"
    language = 'en'
    url = 'http://cagle.com'
    start_date = '2001-01-04'
    rights = 'MSNBC'

class Crawler(CrawlerBase):
    history_capable_date = '2001-01-04'
    time_zone = -5

    def crawl(self, pub_date):
        url = 'http://www.cagle.com/working/%s/cagle00.gif' % (
            pub_date.strftime('%y%m%d'),)
        return CrawlerImage(url)
