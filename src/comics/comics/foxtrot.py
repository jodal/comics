import datetime as dt

from comics.aggregator.crawler import CrawlerResult, GoComicsCrawlerBase
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "FoxTrot"
    language = "en"
    url = "https://www.gocomics.com/foxtrot"
    start_date = "1988-04-10"
    rights = "Bill Amend"


class Crawler(GoComicsCrawlerBase):
    history_capable_date = "2006-12-27"
    schedule = "Su"
    time_zone = "America/Denver"

    def crawl(self, pub_date: dt.date) -> CrawlerResult:
        return self.crawl_helper("foxtrot", pub_date)
