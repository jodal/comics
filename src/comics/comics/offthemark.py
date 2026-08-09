import datetime as dt

from comics.aggregator.crawler import CrawlerResult, GoComicsCrawlerBase
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "Off the Mark"
    language = "en"
    url = "https://www.gocomics.com/offthemark"
    start_date = "2002-09-02"
    rights = "Mark Parisi"


class Crawler(GoComicsCrawlerBase):
    history_capable_date = "2002-09-02"
    schedule = "Mo,Tu,We,Th,Fr,Sa,Su"
    time_zone = "America/New_York"

    def crawl(self, pub_date: dt.date) -> CrawlerResult:
        return self.crawl_helper("offthemark", pub_date)
