# encoding: utf-8

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Pet Peevy'
    language = 'en'
    url = 'http://dobbcomics.com/pp_view'
    rights = 'Rob Snyder'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        page = self.parse_page('http://dobbcomics.com/pp_view')
        url = page.src('img[src*="images/comics/petpeevy/"]')
        return CrawlerImage(url)
