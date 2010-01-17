from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Calvin and Hobbes'
    language = 'en'
    url = 'http://www.calvinandhobbes.com/'
    start_date = '1985-11-18'
    end_date = '1995-12-31'
    rights = 'Bill Watterson'

class Crawler(CrawlerBase):
    history_capable_days = 31
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'

    def crawl(self, pub_date):
        url = 'http://images.ucomics.com/comics/ch/%s.gif' % (
            pub_date.strftime('%Y/ch%y%m%d'),)
        return CrawlerImage(url)
