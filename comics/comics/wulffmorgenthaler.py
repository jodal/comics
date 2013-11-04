from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Wumo'
    language = 'en'
    url = 'http://kindofnormal.com/wumo/'
    start_date = '2001-01-01'
    rights = 'Mikael Wulff & Anders Morgenthaler'


class Crawler(CrawlerBase):
    history_capable_date = '2013-01-15'
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 'Europe/Copenhagen'

    def crawl(self, pub_date):
        page_url = 'http://kindofnormal.com/wumo/' + pub_date.strftime('%Y/%m/%d')
        page = self.parse_page(page_url)
        url = 'http://kindofnormal.com/img/wumo/' + pub_date.strftime('%Y/%m/%d') + '.png'
        title = page.alt('img[src="' + url + '"]')
        return CrawlerImage(url, title)
