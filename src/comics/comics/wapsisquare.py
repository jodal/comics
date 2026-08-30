import datetime as dt

from comics.aggregator.crawler import CrawlerBase, CrawlerImage, CrawlerResult
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "Wapsi Square"
    language = "en"
    url = "http://wapsisquare.com/"
    start_date = "2001-09-09"
    rights = "Paul Taylor"


class Crawler(CrawlerBase):
    history_length_days = 14
    time_zone = "America/Chicago"

    def crawl(self, pub_date: dt.date) -> CrawlerResult:
        feed = self.parse_feed("http://wapsisquare.com/feed/")
        for entry in feed.for_date(pub_date):
            url = entry.summary.src("img")
            title = entry.title
            return CrawlerImage(url, title)
        return None
