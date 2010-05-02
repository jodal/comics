from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Boxer Hockey'
    language = 'en'
    url = 'http://boxerhockey.fireball20xl.com/'
    start_date = '2007-11-25'
    rights = 'Tyson "Rittz" Hesse'

class Crawler(CrawlerBase):
    time_zone = -7

    def crawl(self, pub_date):
        page_url = 'http://boxerhockey.fireball20xl.com/'
        page = self.parse_page(page_url)
        url = page.src('img[src*="comics/"]')
        return CrawlerImage(url)
