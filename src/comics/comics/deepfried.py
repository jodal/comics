import datetime as dt

from comics.aggregator.crawler import CrawlerBase, CrawlerImage, CrawlerResult
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "Deep Fried"
    language = "en"
    url = "http://www.whatisdeepfried.com/"
    start_date = "2001-09-16"
    rights = "Jason Yungbluth"


class Crawler(CrawlerBase):
    history_length_days = 14
    schedule = None
    time_zone = "America/New_York"

    def crawl(self, pub_date: dt.date) -> CrawlerResult:
        feed = self.parse_feed("http://www.whatisdeepfried.com/feed/")
        for entry in feed.for_date(pub_date):
            url = entry.summary.src("img")
            title = entry.title
            return CrawlerImage(url, title)
        return None
