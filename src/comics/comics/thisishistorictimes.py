import datetime as dt

from comics.aggregator.crawler import CrawlerBase, CrawlerImage, CrawlerResult
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "This is Historic Times"
    language = "en"
    url = "http://www.thisishistorictimes.com/"
    start_date = "2006-01-01"
    rights = "Terrence Nowicki, Jr."


class Crawler(CrawlerBase):
    history_length_days = 60
    time_zone = "America/Los_Angeles"

    def crawl(self, pub_date: dt.date) -> CrawlerResult:
        feed = self.parse_feed("http://thisishistorictimes.com/feed/")
        for entry in feed.for_date(pub_date):
            page = self.parse_page(entry.link)
            # The comic is the first image, followed by unrelated ones
            urls = page.srcs('img[src*="/wp-content/uploads/"]')
            if not urls:
                continue
            title = entry.title
            return CrawlerImage(urls[0], title)
        return None
