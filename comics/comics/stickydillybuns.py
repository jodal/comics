from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Sticky Dilly Buns'
    language = 'en'
    url = 'http://www.stickydillybuns.com/'
    start_date = '2013-01-07'
    rights = 'G. Lagace'


class Crawler(CrawlerBase):
    history_capable_date = '2013-01-07'
    schedule = 'Mo,Fr'
    time_zone = 'US/Eastern'

    def crawl(self, pub_date):
        url = 'http://www.stickydillybuns.com/comics/sdb%s.png' % (
            pub_date.strftime('%Y%m%d'))
        return CrawlerImage(url)
