from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Bizarro'
    language = 'en'
    url = 'http://bizarrocomics.com/'
    start_date = '1985-01-01'
    rights = 'Dan Piraro'


class Crawler(CrawlerBase):
    history_capable_days = 40
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 'US/Eastern'


    def crawl(self, pub_date):
        dom = pub_date.strftime('%B-')+pub_date.strftime('%d-').lstrip("0")+pub_date.strftime("%Y")
        page_url = 'http://bizarro.com/comics/' + dom + '/'
        page = self.parse_page(page_url)
        url = page.src('img[src^="https://safr.kingfeatures.com/"]')
        return CrawlerImage(url)
