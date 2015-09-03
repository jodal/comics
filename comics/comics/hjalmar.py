from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Hjalmar'
    language = 'no'
    url = 'http://heltnormalt.no/hjalmar'
    rights = 'Nils Axle Kanten'


class Crawler(CrawlerBase):
    history_capable_date = '2013-01-15'
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 'Europe/Oslo'

    def crawl(self, pub_date):
        date_string = pub_date.strftime('%Y/%m/%d')
        page_url = 'http://heltnormalt.no/hjalmar/%s' % date_string
        page = self.parse_page(page_url)
        url = page.src('img[src*="/img/hjalmar/%s"]' % date_string)
        return CrawlerImage(url)
