from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Dustin'
    language = 'en'
    url = 'http://dustincomics.com'
    start_date = '2010-01-04'
    rights = 'Steve Kelley & Jeff Parker'


class Crawler(CrawlerBase):
    history_capable_date = '2010-01-04'
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 'US/Eastern'

    def crawl(self, pub_date):
        date = pub_date.strftime('%B-')
        date += pub_date.strftime('%d').lstrip('0')
        date += pub_date.strftime('-%Y')
        page_url = 'http://dustincomics.com/comics/' + date
        page = self.parse_page(page_url)
        url = page.src('img[src*="safr.kingfeatures.com"]')
        return CrawlerImage(url)
