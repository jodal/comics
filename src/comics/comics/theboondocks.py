import datetime as dt

from comics.aggregator.crawler import CrawlerResult, GoComicsCrawlerBase
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "The Boondocks"
    language = "en"
    url = "https://www.gocomics.com/boondocks"
    start_date = "1999-04-19"
    rights = "Aaron McGruder"


class Crawler(GoComicsCrawlerBase):
    history_capable_date = "1999-04-19"
    schedule = "Mo,Tu,We,Th,Fr,Sa,Su"
    time_zone = "America/Denver"

    def crawl(self, pub_date: dt.date) -> CrawlerResult:
        return self.crawl_helper("boondocks", pub_date)
