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
    history_start_date = "2001-12-19"
    schedule = "Mo,Tu,We,Th,Fr"
    time_zone = "America/Chicago"

    def crawl(self, pub_date: dt.date) -> CrawlerResult:
        url = f"https://somethingpositive.net/sp{pub_date:%m%d%Y}.png"
        return CrawlerImage(url)
