import datetime as dt

from comics.aggregator.crawler import CrawlerBase, CrawlerImage, CrawlerResult
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "Lunch (e24.no)"
    language = "no"
    url = "https://www.e24.no/"
    start_date = "2009-10-21"
    rights = "Børge Lund"


class Crawler(CrawlerBase):
    history_start_date = "2024-05-02"
    schedule = "Mo,Tu,We,Th,Fr,Sa"
    time_zone = "Europe/Oslo"

    def crawl(self, pub_date: dt.date) -> CrawlerResult:
        url = f"https://api.strandcomics.no/striper/e24/lunch/{pub_date:%Y-%m-%d}"
        return CrawlerImage(url)
