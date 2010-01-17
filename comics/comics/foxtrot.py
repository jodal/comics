from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'FoxTrot'
    language = 'en'
    url = 'http://www.foxtrot.com/'
    start_date = '1988-04-10'
    rights = 'Bill Amend'

class Crawler(CrawlerBase):
    history_capable_date = '2006-12-27'
    schedule = 'Su'
    time_zone = -5

    def crawl(self, pub_date):
        url = 'http://images.ucomics.com/comics/ft/%s.gif' % (
            pub_date.strftime('%Y/ft%y%m%d'),)
        return CrawlerImage(url)
