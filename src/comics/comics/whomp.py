import datetime as dt

from comics.aggregator.crawler import ComicControlCrawlerBase, CrawlerResult
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "Whomp!"
    language = "en"
    url = "http://www.whompcomic.com/"
    start_date = "2010-06-14"
    rights = "Ronnie Filyaw"


class Crawler(ComicControlCrawlerBase):
    history_capable_days = 70
    schedule = "Mo,We,Fr"
    time_zone = "America/New_York"

    def crawl(self, pub_date: dt.date) -> CrawlerResult:
        return self.crawl_helper(Metadata.url, pub_date)
