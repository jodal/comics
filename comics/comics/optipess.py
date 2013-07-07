# encoding: utf-8

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Optipess'
    language = 'en'
    url = 'http://www.optipess.com/'
    start_date = '2008-12-01'
    rights = 'Kristian Nygård'


class Crawler(CrawlerBase):
    history_capable_days = 90
    schedule = 'Th,Su'
    time_zone = 'Europe/Oslo'

    def crawl(self, pub_date):
        feed = self.parse_feed('http://feeds.feedburner.com/Optipess')
        for entry in feed.for_date(pub_date):
            if 'Comic' not in entry.tags:
                continue
            url = entry.summary.src('img[src*="/comics/"]')
            title = entry.title
            return CrawlerImage(url, title)
