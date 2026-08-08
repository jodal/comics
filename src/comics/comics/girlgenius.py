import datetime as dt

from comics.aggregator.crawler import CrawlerBase, CrawlerImage, CrawlerResult
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "Girl Genius"
    language = "en"
    url = "https://www.girlgeniusonline.com/"
    start_date = "2002-11-04"
    rights = "Studio Foglio, LLC"


class Crawler(CrawlerBase):
    history_capable_date = "2002-11-04"
    schedule = "Mo,We,Fr"
    time_zone = "America/Los_Angeles"

    def crawl(self, pub_date: dt.date) -> CrawlerResult:
        url = (
            "https://www.girlgeniusonline.com/ggmain/strips/"
            f"ggmain{pub_date:%Y%m%d}b.jpg"
        )
        return CrawlerImage(url)
