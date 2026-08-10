import datetime as dt

from comics.aggregator.crawler import CrawlerBase, CrawlerImage, CrawlerResult
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "General Protection Fault"
    language = "en"
    url = "https://www.gpf-comics.com/"
    start_date = "1998-11-02"
    rights = "Jeffrey T. Darlington"


class Crawler(CrawlerBase):
    history_start_date = "1998-11-02"
    schedule = "Mo"
    time_zone = "America/New_York"

    def crawl(self, pub_date: dt.date) -> CrawlerResult:
        page_url = f"https://www.gpf-comics.com/archive.php?d={pub_date:%Y%m%d}"
        page = self.parse_page(page_url)
        url = page.src('img[alt^="[Comic for"]')
        return CrawlerImage(url)
