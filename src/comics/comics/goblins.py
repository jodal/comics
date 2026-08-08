import datetime as dt

from comics.aggregator.crawler import ComicControlCrawlerBase, CrawlerResult
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "Goblins"
    language = "en"
    url = "http://www.goblinscomic.com/"
    start_date = "2005-05-29"
    rights = "Tarol Hunt"


class Crawler(ComicControlCrawlerBase):
    history_capable_days = 30
    time_zone = "America/Los_Angeles"

    def crawl(self, pub_date: dt.date) -> CrawlerResult:
        return self.crawl_helper(Metadata.url, pub_date)
