from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'Mutts'
    language = 'en'
    url = 'http://muttscomics.com'
    start_date = '1994-01-01'
    rights = 'Patrick McDonnell'

class Crawler(CrawlerBase):
    history_capable_date = '1994-09-11'
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'

    def crawl(self, pub_date):
        url = 'http://muttscomics.com/art/images/daily/%s.gif' % (
            pub_date.strftime('%m%d%y'),)
        return CrawlerImage(url)
