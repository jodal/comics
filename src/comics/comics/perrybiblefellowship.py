import datetime as dt

from comics.aggregator.crawler import CrawlerBase, CrawlerImage, CrawlerResult
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "The Perry Bible Fellowship"
    language = "en"
    url = "https://pbfcomics.com/"
    start_date = "2001-01-01"
    rights = "Nicholas Gurewitch"


class Crawler(CrawlerBase):
    history_start_date = "2019-06-12"
    time_zone = "America/New_York"

    def crawl(self, pub_date: dt.date) -> CrawlerResult:
        feed = self.parse_feed("https://pbfcomics.com/feed/")
        for entry in feed.for_date(pub_date):
            page = self.parse_page(entry.link)
            urls = page.attrs("data-src", "div#comic > img")
            return [CrawlerImage(url, entry.title) for url in urls]
        return None
