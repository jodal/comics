from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Wumo'
    language = 'en'
    url = 'http://wumo.com/wumo/'
    start_date = '2001-01-01'
    rights = 'Mikael Wulff & Anders Morgenthaler'


class Crawler(CrawlerBase):
    history_capable_date = '2010-01-01'
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 'Europe/Copenhagen'
    headers = {'Referer': 'http://wumo.com/', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36' }

    def crawl(self, pub_date):
        page_url = 'http://wumo.com/wumo/%s' % (
            pub_date.strftime('%Y/%m/%d'),)
        page = self.parse_page(page_url)
        url = page.href('link[rel="image_src"]')
        title = page.alt('img[src*="%s"]' % url)
        return CrawlerImage(url, title)
