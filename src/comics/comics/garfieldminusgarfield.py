import datetime as dt

from comics.aggregator.crawler import CrawlerBase, CrawlerImage, CrawlerResult
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "Garfield minus Garfield"
    language = "en"
    url = "http://garfieldminusgarfield.tumblr.com/"
    rights = "Travors"


class Crawler(CrawlerBase):
    history_length_days = 30
    schedule = None
    time_zone = "Europe/London"

    def crawl(self, pub_date: dt.date) -> CrawlerResult:
        feed = self.parse_feed("http://garfieldminusgarfield.tumblr.com/rss")
        for entry in feed.for_date(pub_date):
            url = entry.summary.src("img")
            return CrawlerImage(url)
        return None
