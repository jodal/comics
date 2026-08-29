import datetime as dt

from comics.aggregator.crawler import CrawlerBase, CrawlerImage, CrawlerResult
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "Something Positive"
    language = "en"
    url = "https://somethingpositive.net/"
    start_date = "2001-12-19"
    rights = "R. K. Milholland"


class Crawler(CrawlerBase):
    history_length_days = 30
    time_zone = "America/Chicago"

    def crawl(self, pub_date: dt.date) -> CrawlerResult:
        feed = self.parse_feed("https://somethingpositive.net/feed/")
        for entry in feed.for_date(pub_date):
            page = self.parse_page(entry.link)
            url = page.src('img[src*="comics/sp"]')
            if url is None:
                continue
            return CrawlerImage(url, entry.title)
        return None
