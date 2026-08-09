import datetime as dt

from comics.aggregator.crawler import CrawlerBase, CrawlerImage, CrawlerResult
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "The Devil Bear"
    language = "en"
    url = "http://www.thedevilbear.com/"
    start_date = "2009-01-01"
    rights = "Ben Bourbon"


class Crawler(CrawlerBase):
    history_length_days = 0
    schedule = "Tu,We,Th,Fr"
    time_zone = "America/New_York"

    def crawl(self, pub_date: dt.date) -> CrawlerResult:
        page = self.parse_page("http://www.thedevilbear.com/")
        url = page.src("#comic img")
        return CrawlerImage(url)
