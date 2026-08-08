import datetime as dt

from comics.aggregator.crawler import ComicControlCrawlerBase, CrawlerResult
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "Three Panel Soul"
    language = "en"
    url = "http://www.threepanelsoul.com/"
    start_date = "2006-11-05"
    rights = "Ian McConville & Matt Boyd"


class Crawler(ComicControlCrawlerBase):
    history_capable_days = 180
    schedule = "Mo"
    time_zone = "America/New_York"

    def crawl(self, pub_date: dt.date) -> CrawlerResult:
        return self.crawl_helper(Metadata.url, pub_date)
