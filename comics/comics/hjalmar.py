from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Hjalmar'
    language = 'no'
    url = 'http://heltnormalt.no/hjalmar'
    rights = 'Nils Axle Kanten'


class Crawler(CrawlerBase):
    history_capable_date = '2013-01-15'
    time_zone = 'Europe/Oslo'

    def crawl(self, pub_date):
        url = 'http://heltnormalt.no/img/hjalmar/%s.jpg' % (
            pub_date.strftime('%Y/%m/%d'))
        return CrawlerImage(url)
