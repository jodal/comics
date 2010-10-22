from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

import re

class Meta(MetaBase):
    name = 'Questionable Content'
    language = 'en'
    url = 'http://questionablecontent.net/'
    start_date = '2003-08-01'
    rights = 'Jeph Jacques'

class Crawler(CrawlerBase):
    schedule = 'Mo,Tu,We,Th,Fr'
    time_zone = -6

    def crawl(self, pub_date):
        page = self.parse_page('http://www.questionablecontent.net/')
        if pub_date.strftime('%B %d, %Y') in page.text('div#news'):
            url = page.src('img#strip')
            title = None
            text = re.sub(r'\s{2,}', '\n\n', page.text('div#news')).strip()
            return CrawlerImage(url, title, text)
