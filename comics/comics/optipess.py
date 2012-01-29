# encoding: utf-8

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Optipess'
    language = 'en'
    url = 'http://www.optipess.com/'
    start_date = '2008-12-01'
    rights = 'Kristian Nygård'

class Crawler(CrawlerBase):
    history_capable_days = 90
    schedule = 'Th,Su'
    time_zone = -7

    def crawl(self, pub_date):
        feed = self.parse_feed(
            'http://feeds.feedburner.com/Optipess?format=xml')
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img[src*="/comics/"]')
            title = entry.title
            return CrawlerImage(url, title)
