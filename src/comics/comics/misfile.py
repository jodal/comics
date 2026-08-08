import datetime as dt

from comics.aggregator.crawler import ComicControlCrawlerBase, CrawlerResult
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "Misfile"
    language = "en"
    url = "http://www.misfile.com/"
    start_date = "2004-03-01"
    rights = "Chris Hazelton"


class Crawler(ComicControlCrawlerBase):
    history_capable_days = 10
    schedule = "Mo,Tu,We,Th,Fr"
    time_zone = "America/New_York"

    def crawl(self, pub_date: dt.date) -> CrawlerResult:
        return self.crawl_helper(Metadata.url, pub_date)
