import datetime as dt

from comics.aggregator.crawler import CrawlerResult, GoComicsCrawlerBase
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "Crabgrass"
    language = "en"
    url = "https://www.gocomics.com/crabgrass"
    rights = "Tauhid Bondia"


class Crawler(GoComicsCrawlerBase):
    history_capable_date = "2019-04-05"
    schedule = "Mo,Tu,We,Th,Fr,Sa,Su"
    time_zone = "America/New_York"

    def crawl(self, pub_date: dt.date) -> CrawlerResult:
        return self.crawl_helper("crabgrass", pub_date)
