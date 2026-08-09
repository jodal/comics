import datetime as dt

from comics.aggregator.crawler import CrawlerResult, GoComicsCrawlerBase
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "Luann"
    language = "en"
    url = "https://www.gocomics.com/luann"
    rights = "Greg Evans and Karen Evans"


class Crawler(GoComicsCrawlerBase):
    history_capable_date = "1985-03-17"
    schedule = "Mo,Tu,We,Th,Fr,Sa,Su"
    time_zone = "America/New_York"

    def crawl(self, pub_date: dt.date) -> CrawlerResult:
        return self.crawl_helper("luann", pub_date)
