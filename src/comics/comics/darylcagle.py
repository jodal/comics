import datetime as dt

from comics.aggregator.crawler import CrawlerBase, CrawlerImage, CrawlerResult
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "Daryl Cagle's Political Blog"
    language = "en"
    url = "http://www.cagle.com/"
    start_date = "2001-01-04"
    rights = "Daryl Cagle"


class Crawler(CrawlerBase):
    history_length_days = 365
    time_zone = "America/Los_Angeles"
    # The image server rejects the bare "Mozilla/5.0" user agent
    headers = {"User-Agent": "Mozilla/5.0 (Linux)"}

    def crawl(self, pub_date: dt.date) -> CrawlerResult:
        feed = self.parse_feed("https://cagle.com/daryl-cagle/feed/")
        for entry in feed.for_date(pub_date):
            url = entry.content0.src("img")
            title = entry.title
            return CrawlerImage(url, title)
        return None
