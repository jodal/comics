# encoding: utf-8

import re
import urllib

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Lunch'
    language = 'no'
    url = 'http://lunchstriper.lunddesign.no/'
    start_date = '2009-10-21'
    rights = 'Børge Lund'

class Crawler(CrawlerBase):
    time_zone = 1
    history_capable_date = '2009-04-01'

    def crawl(self, pub_date):
        page = self.parse_page('http://lunchstriper.lunddesign.no/comics/')
        url = page.href('a[href*="comics/%s"]' % pub_date.strftime('%Y-%m-%d'))

        if not url:
            return

        title = re.sub('^http://lunchstriper.lunddesign.no/comics/' +
            '\d{4}-\d{2}-\d{2}(-LUNCH_\d+)?-?', '', url or '')
        title = re.sub('(_farger)?\.png$', '', title)
        title = urllib.unquote(title).encode('iso-8859-1').decode('utf-8')
        title = title.replace('_', ' ').strip()

        if title:
            title = title[0].upper() + title[1:]

        return CrawlerImage(url, title or None)
