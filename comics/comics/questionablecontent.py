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
    history_capable_days = 0
    schedule = 'Mo,Tu,We,Th,Fr'
    time_zone = -6

    def crawl(self, pub_date):
        check_date = pub_date.strftime(r'%B %d, %Y')

        page = self.parse_page('http://www.questionablecontent.net/')
        if check_date in page.text('div#news'):
            title = None
            text_formatter = re.compile('[ 	\n]{2,}')
            text = text_formatter.sub('\n\n', page.text('div#news')).strip()
            url = page.src('img#strip')

            return CrawlerImage(url, title, text)
