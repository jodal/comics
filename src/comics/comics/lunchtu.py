import datetime as dt

from comics.aggregator.crawler import CrawlerBase, CrawlerImage, CrawlerResult
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "Lunch (tu.no)"
    language = "no"
    url = "https://www.tu.no/lunch/"
    start_date = "2009-10-21"
    rights = "Børge Lund"


class Crawler(CrawlerBase):
    history_length_days = 20
    schedule = "Mo,Tu,We,Th,Fr"
    time_zone = "Europe/Oslo"

    def crawl(self, pub_date: dt.date) -> CrawlerResult:
        url = (
            f"https://www.tu.no/api/widgets/comics?name=lunch&date={pub_date:%Y-%m-%d}"
        )
        return CrawlerImage(url)
