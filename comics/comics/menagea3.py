# encoding: utf-8

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'Ménage à 3'
    language = 'en'
    url = 'http://www.menagea3.net/'
    start_date = '2008-05-17'
    rights = 'Giz & Dave Zero 1'

class Crawler(CrawlerBase):
    history_capable_date = '2008-05-17'
    schedule = 'Tu,Th,Sa'
    time_zone = -8

    def crawl(self, pub_date):
        url = 'http://zii.menagea3.net/comics/mat%s.png' % (
            pub_date.strftime('%Y%m%d'))
        return CrawlerImage(url)
