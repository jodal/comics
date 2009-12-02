import re

from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'The Joy of Tech'
    language = 'en'
    url = 'http://www.geekculture.com/joyoftech/'
    start_date = '2000-08-14'
    history_capable_days = 30
    schedule = 'Mo,We,Fr'
    time_zone = -5
    rights = 'Geek Culture'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        feed = self.parse_feed(
            'http://www.joyoftech.com/joyoftech/jotblog/atom.xml')
        for entry in feed.for_date(pub_date):
            page = self.parse_page(entry.link)
            url = page.src('img[alt="The Joy of Tech comic"]')
            title = entry.title
            return CrawlerResult(url, title)
