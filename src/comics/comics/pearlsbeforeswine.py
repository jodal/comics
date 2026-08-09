import datetime as dt

from comics.aggregator.crawler import CrawlerResult, GoComicsCrawlerBase
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "Pearls Before Swine"
    language = "en"
    url = "https://www.gocomics.com/pearlsbeforeswine"
    start_date = "2001-12-30"
    rights = "Stephan Pastis"


class Crawler(GoComicsCrawlerBase):
    history_capable_date = "2002-01-06"
    schedule = "Mo,Tu,We,Th,Fr,Sa,Su"
    time_zone = "America/New_York"

    def crawl(self, pub_date: dt.date) -> CrawlerResult:
        return self.crawl_helper("pearlsbeforeswine", pub_date)
