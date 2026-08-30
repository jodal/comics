import datetime as dt

from comics.aggregator.crawler import CrawlerBase, CrawlerImage, CrawlerResult
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "Exiern"
    language = "en"
    url = "https://exiern.thecomicseries.com/"
    start_date = "2005-09-06"
    rights = "Dan Standing"


class Crawler(CrawlerBase):
    history_length_days = 30
    time_zone = "America/New_York"

    def crawl(self, pub_date: dt.date) -> CrawlerResult:
        feed = self.parse_feed("https://exiern.thecomicseries.com/rss/")
        for entry in feed.for_date(pub_date):
            page = self.parse_page(entry.link)
            url = page.src('img[src*="img.comicfury.com/comics/"]')
            if url is None:
                continue
            title = entry.title
            return CrawlerImage(url, title)
        return None
