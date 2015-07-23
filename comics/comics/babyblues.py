from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Baby Blues'
    language = 'en'
    url = 'http://www.babyblues.com'
    start_date = '1990-01-01'
    rights = 'Rick Kirkman and Jerry Scott'


class Crawler(CrawlerBase):
    history_capable_date = '1995-01-08'
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 'US/Eastern'

    def crawl(self, pub_date):
        date = pub_date.strftime('%B-')
        date += pub_date.strftime('%d').lstrip('0')
        date += pub_date.strftime('-%Y')
        page_url = 'http://babyblues.com/comics/' + date
        page = self.parse_page(page_url)
        url = page.src('img[src*="safr.kingfeatures.com"]')
        return CrawlerImage(url)
