from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'Mutts (start.no)'
    language = 'no'
    url = 'http://www.start.no/tegneserier/'
    start_date = '1994-01-01'
    rights = 'Patrick McDonnell'

class Crawler(CrawlerBase):
    
    history_capable_date = '2009-03-23'
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 'Europe/Oslo'

    def crawl(self, pub_date):
        url = 'http://g2.start.no/tegneserier/striper/mutts/MUT%s.gif' % (
            pub_date.strftime('%Y%m%d'),)
        return CrawlerImage(url)
