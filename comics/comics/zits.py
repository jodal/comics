from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Zits'
    language = 'en'
    url = 'http://zitscomics.com/'
    start_date = '1997-07-01'
    rights = 'Jerry Scott and Jim Borgman'


class Crawler(CrawlerBase):
    history_capable_date = '2005-01-01'
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 'US/Eastern'

    def crawl(self, pub_date):
        date = pub_date.strftime('%B-')
        date = date + pub_date.strftime('%d').lstrip('0')
        date = date + pub_date.strftime('-%Y')
        page_url = 'http://zitscomics.com/comics/' + date
        page = self.parse_page(page_url)

        url = page.src('img[src*="safr.kingfeatures.com"]')

        return CrawlerImage(url)
