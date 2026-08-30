import datetime as dt

from comics.aggregator.crawler import CrawlerBase, CrawlerImage, CrawlerResult
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "Basic Instructions"
    language = "en"
    url = "http://www.basicinstructions.net/"
    start_date = "2006-07-01"
    rights = "Scott Meyer"


class Crawler(CrawlerBase):
    history_length_days = 100
    schedule = "Mo"
    time_zone = "America/New_York"

    def crawl(self, pub_date: dt.date) -> CrawlerResult:
        feed = self.parse_feed(
            "http://basicinstructions.net/basic-instructions/rss.xml"
        )
        for entry in feed.for_date(pub_date):
            url = entry.summary.src("img")
            if url is None:
                continue
            # The size in the query limits the image that the CDN serves
            url = url.split("?")[0]
            title = entry.title
            return CrawlerImage(url, title)
        return None
