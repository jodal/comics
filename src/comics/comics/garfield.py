import datetime as dt

from comics.aggregator.crawler import CrawlerResult, GoComicsCrawlerBase
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "Garfield"
    language = "en"
    url = "https://www.gocomics.com/garfield"
    start_date = "1978-06-19"
    rights = "Jim Davis"


class Crawler(GoComicsCrawlerBase):
    history_capable_date = "1978-06-19"
    schedule = "Mo,Tu,We,Th,Fr,Sa,Su"
    time_zone = "America/New_York"

    def crawl(self, pub_date: dt.date) -> CrawlerResult:
        return self.crawl_helper("garfield", pub_date)
