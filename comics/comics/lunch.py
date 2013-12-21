# encoding: utf-8

import re
import urllib

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Lunch'
    language = 'no'
    url = 'http://lunchstriper.lunddesign.no/'
    start_date = '2009-10-21'
    rights = 'Børge Lund'


class Crawler(CrawlerBase):
    history_capable_date = '2009-04-01'
    time_zone = 'Europe/Oslo'

    def crawl(self, pub_date):
        feed = self.parse_feed('http://lunchstriper.lunddesign.no/?feed=rss2')
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img[src*="/comics/"]')
            title = entry.title
            return CrawlerImage(url, title)
