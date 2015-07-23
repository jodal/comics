from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Beetle Bailey'
    language = 'en'
    url = 'http://beetlebailey.com'
    start_date = '1950-01-01'
    rights = 'Mort Walker'


class Crawler(CrawlerBase):
    history_capable_date = '1996-07-07'
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 'US/Eastern'

    def crawl(self, pub_date):
        date = pub_date.strftime('%B-')
        date += pub_date.strftime('%d').lstrip('0')
        date += pub_date.strftime('-%Y')
        page_url = 'http://beetlebailey.com/comics/' + date
        page = self.parse_page(page_url)
        url = page.src('img[src*="safr.kingfeatures.com"]')
        return CrawlerImage(url)
