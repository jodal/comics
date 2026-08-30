import datetime as dt

from comics.aggregator.crawler import CrawlerBase, CrawlerImage, CrawlerResult
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "Least I Could Do"
    language = "en"
    url = "https://www.leasticoulddo.com/"
    start_date = "2003-02-10"
    rights = "Ryan Sohmer & Lar deSouza"


class Crawler(CrawlerBase):
    history_length_days = 10
    schedule = "Mo,Tu,We,Th,Fr,Sa,Su"
    time_zone = "America/Montreal"

    def crawl(self, pub_date: dt.date) -> CrawlerResult:
        feed = self.parse_feed("https://leasticoulddo.com/feed/")
        for entry in feed.for_date(pub_date):
            page = self.parse_page(entry.link)
            url = page.content('meta[property="og:image"]')
            return CrawlerImage(url, entry.title)
        return None
