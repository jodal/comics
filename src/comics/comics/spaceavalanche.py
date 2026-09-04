import datetime as dt

from comics.aggregator.crawler import CrawlerBase, CrawlerImage, CrawlerResult
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "Space Avalanche"
    language = "en"
    url = "http://www.spaceavalanche.com/"
    start_date = "2009-02-02"
    rights = "Eoin Ryan"
    active = False


class Crawler(CrawlerBase):
    history_length_days = 365
    time_zone = "Europe/Dublin"

    def crawl(self, pub_date: dt.date) -> CrawlerResult:
        feed = self.parse_feed("http://feeds.feedburner.com/SpaceAvalanche")
        for entry in feed.for_date(pub_date):
            if "COMIC ARCHIVE" not in entry.tags:
                continue
            url = entry.content0.src('img[src*="/wp-content/uploads/"]', first=True)
            title = entry.title
            return CrawlerImage(url, title)
        return None
