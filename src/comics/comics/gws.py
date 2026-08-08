import datetime as dt

from comics.aggregator.crawler import ComicControlCrawlerBase, CrawlerResult
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "Girls With Slingshots"
    language = "en"
    url = "http://www.girlswithslingshots.com/"
    start_date = "2004-09-30"
    rights = "Danielle Corsetto"


class Crawler(ComicControlCrawlerBase):
    history_capable_days = 30
    schedule = "Mo,Tu,We,Th,Fr"
    time_zone = "America/New_York"

    def crawl(self, pub_date: dt.date) -> CrawlerResult:
        return self.crawl_helper(Metadata.url, pub_date)
