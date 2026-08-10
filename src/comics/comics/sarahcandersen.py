import datetime as dt

from comics.aggregator.crawler import CrawlerBase, CrawlerImage, CrawlerResult
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "Sarah's Scribbles"
    language = "en"
    url = "http://www.sarahcandersen.com/"
    start_date = "2011-01-01"
    rights = "Sarah Andersen"


class Crawler(CrawlerBase):
    history_length_days = 60
    schedule = "We,Sa"
    time_zone = "America/New_York"

    def crawl(self, pub_date: dt.date) -> CrawlerResult:
        feed = self.parse_feed("http://sarahcandersen.com/rss")
        for entry in feed.for_date(pub_date):
            return [CrawlerImage(url) for url in entry.summary.srcs('img[src*="_500"]')]
        return None
