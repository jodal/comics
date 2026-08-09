import datetime as dt

from comics.aggregator.crawler import CrawlerResult, GoComicsCrawlerBase
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "Get Fuzzy"
    language = "en"
    url = "https://www.gocomics.com/getfuzzy"
    start_date = "1999-09-01"
    rights = "Darby Conley"


class Crawler(GoComicsCrawlerBase):
    history_capable_date = "2009-05-26"
    schedule = "Mo,Tu,We,Th,Fr,Sa,Su"
    time_zone = "America/Denver"

    def crawl(self, pub_date: dt.date) -> CrawlerResult:
        return self.crawl_helper("getfuzzy", pub_date)
