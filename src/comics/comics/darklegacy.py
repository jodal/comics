import datetime as dt

from comics.aggregator.crawler import CrawlerBase, CrawlerImage, CrawlerResult
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "Dark Legacy"
    language = "en"
    url = "http://www.darklegacycomics.com/"
    start_date = "2006-01-01"
    rights = "Arad Kedar"


class Crawler(CrawlerBase):
    history_length_days = 33 * 7  # 33 weekly releases
    schedule = "Su"
    time_zone = "America/Los_Angeles"

    def crawl(self, pub_date: dt.date) -> CrawlerResult:
        feed = self.parse_feed("http://www.darklegacycomics.com/feed.xml")
        for entry in feed.for_date(pub_date):
            title = entry.title
            page = self.parse_page(entry.link)
            url = page.src(".comic img")
            return CrawlerImage(url, title)
        return None
