# encoding: utf-8

from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Kukuburi'
    language = 'en'
    url = 'http://www.kukuburi.com/'
    start_date = '2007-09-08'
    history_capable_days = 60
    schedule = 'Tu,Th'
    time_zone = -8
    rights = 'Ramón Pérez'

class ComicCrawler(BaseComicCrawler):
    def crawl(self):
        feed = self.parse_feed('http://feeds2.feedburner.com/Kukuburi')
        for entry in feed.for_day(self.pub_date):
            self.url = entry.summary.src('img[src*="/comics/"]')
            self.title = entry.title
