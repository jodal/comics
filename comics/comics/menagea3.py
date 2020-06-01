# encoding: utf-8

import datetime

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Ménage à 3"
    language = "en"
    url = "http://www.ma3comic.com/"
    start_date = "2008-05-17"
    rights = "Giz & Dave Zero 1"
    active = False


class Crawler(CrawlerBase):
    history_capable_days = 50
    schedule = "Tu,Th,Sa"
    time_zone = "US/Eastern"

    def crawl(self, pub_date):
        # Release to the feed is one day delayed, so we try to get yesterday's
        # comic instead.
        pub_date -= datetime.timedelta(days=1)

        feed = self.parse_feed("http://www.ma3comic.com/comic.rss")
        for entry in feed.for_date(pub_date):
            title = entry.title.replace("Menage a 3 - ", "")
            page = self.parse_page(entry.link)
            url = page.src("#cc img")
            return CrawlerImage(url, title)
