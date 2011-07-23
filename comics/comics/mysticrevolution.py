from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

import re

class Meta(MetaBase):
    name = 'Mystic Revolution'
    language = 'en'
    url = 'http://mysticrev.com/'
    start_date = '2004-01-01'
    rights = 'Jennifer Brazas'

class Crawler(CrawlerBase):
    history_capable_days = 0
    schedule = 'Mo,Tu,We,Th,Fr'
    time_zone = -6

    def crawl(self, pub_date):
        page = self.parse_page('http://mysticrev.com/index.php')
        url = page.src('div#comic img')
        title = page.alt('div#comic img')
        return CrawlerImage(url, title, None)
