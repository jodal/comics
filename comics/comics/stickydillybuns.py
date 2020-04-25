import datetime

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Sticky Dilly Buns"
    language = "en"
    url = "http://www.stickydillybuns.com/"
    start_date = "2013-01-07"
    rights = "G. Lagace"


class Crawler(CrawlerBase):
    history_capable_days = 50
    schedule = "Mo,Fr"
    time_zone = "US/Eastern"

    def crawl(self, pub_date):
        # Release to the feed is one day delayed, so we try to get yesterday's
        # comic instead.
        pub_date -= datetime.timedelta(days=1)

        feed = self.parse_feed("http://www.stickydillybuns.com/comic.rss")
        for entry in feed.for_date(pub_date):
            title = entry.title.replace("Sticky Dilly Buns - ", "")
            page = self.parse_page(entry.link)
            url = page.src("#comic img")
            return CrawlerImage(url, title)
