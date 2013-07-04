# encoding: utf-8

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Kukuburi'
    language = 'en'
    url = 'http://www.kukuburi.com/'
    start_date = '2007-09-08'
    rights = 'Ramón Pérez'


class Crawler(CrawlerBase):
    history_capable_days = 60
    schedule = None
    time_zone = 'US/Pacific'

    def crawl(self, pub_date):
        feed = self.parse_feed('http://feeds2.feedburner.com/Kukuburi')
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img[src*="/comics/"]')
            title = entry.title
            return CrawlerImage(url, title)
