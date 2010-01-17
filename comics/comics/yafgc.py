from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Yet Another Fantasy Gamer Comic'
    language = 'en'
    url = 'http://yafgc.shipsinker.com/'
    start_date = '2006-05-29'
    rights = 'Rich Morris'

class Crawler(CrawlerBase):
    history_capable_date = '2006-05-29'
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = -8

    def crawl(self, pub_date):
        url = 'http://yafgc.shipsinker.com/istrip_files/strips/%s.jpg' % (
            pub_date.strftime('%Y%m%d'),)
        return CrawlerImage(url)
