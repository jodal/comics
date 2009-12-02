# encoding: utf-8

from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Kukuburi'
    language = 'en'
    url = 'http://www.kukuburi.com/'
    start_date = '2007-09-08'
    rights = 'Ramón Pérez'

class Crawler(CrawlerBase):
    history_capable_days = 60
    schedule = 'Tu,Th'
    time_zone = -8

    def crawl(self, pub_date):
        feed = self.parse_feed('http://feeds2.feedburner.com/Kukuburi')
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img[src*="/comics/"]')
            title = entry.title
            return CrawlerResult(url, title)
