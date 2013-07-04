from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Sinfest'
    language = 'en'
    url = 'http://www.sinfest.net/'
    start_date = '2001-01-17'
    rights = 'Tatsuya Ishida'


class Crawler(CrawlerBase):
    history_capable_date = '2001-01-17'
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 'US/Eastern'

    def crawl(self, pub_date):
        url = 'http://www.sinfest.net/comikaze/comics/%s.gif' % (
            pub_date.strftime('%Y-%m-%d'),)
        return CrawlerImage(url)
