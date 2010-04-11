from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Wulffmorgenthaler (ap.no)'
    language = 'no'
    url = 'http://www.aftenposten.no/tegneserier/'
    start_date = '2001-01-01'
    rights = 'Mikael Wulff & Anders Morgenthaler'

class Crawler(CrawlerBase):
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 1

    def crawl(self, pub_date):
        page = self.parse_page('http://www.aftenposten.no/tegneserier/')
        url = page.src('img#theCartoon')
        return CrawlerImage(url)
